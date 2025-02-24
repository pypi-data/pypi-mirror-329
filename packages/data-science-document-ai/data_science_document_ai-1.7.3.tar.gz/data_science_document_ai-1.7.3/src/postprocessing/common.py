import asyncio
import datetime
import json
import os
import re
from datetime import timezone

import numpy as np
import pandas as pd
import requests
from vertexai.preview.language_models import TextEmbeddingModel

from src.constants import formatting_rules
from src.io import get_storage_client, logger
from src.prompts.prompt_library import prompt_library
from src.tms import call_tms, set_tms_service_token

tms_domain = os.environ["TMS_DOMAIN"]


class EmbeddingsManager:  # noqa: D101
    def __init__(self, params):  # noqa: D107
        self.params = params
        self.embeddings_dict = {}
        self.embed_model = setup_embed_model()
        self.bucket = self.get_bucket_storage()

    def get_bucket_storage(self):
        """
        Retrieve the bucket storage object.

        Returns:
            The bucket storage object.
        """
        params = self.params
        storage_client = get_storage_client(params)
        bucket = storage_client.bucket(params["doc_ai_bucket_name"])
        return bucket

    def load_embeddings(self):
        """
        Load embeddings for container types, ports, and terminals.

        Returns:
            None
        """
        for data_field in ["container_types", "ports", "terminals", "depots"]:
            self.embeddings_dict[data_field] = load_embed_by_data_field(
                self.bucket, f"embeddings/{data_field}/output"
            )

    async def update_embeddings(self):
        """
        Update the embeddings dictionary.

        Returns:
            dict: The updated embeddings dictionary with the following keys:
                - "container_types": A tuple containing the container types and their embeddings.
                - "ports": A tuple containing the ports and their embeddings.
                - "terminals": A tuple containing the terminal IDs and their embeddings.
        """
        # Update embeddings dict here.
        # Ensure this method is async if you're calling async operations.
        set_tms_service_token()
        container_types, container_type_embeddings = setup_container_type_embeddings(
            self.bucket, self.embed_model, *self.embeddings_dict["container_types"]
        )

        ports, port_embeddings = setup_ports_embeddings(
            self.bucket, self.embed_model, *self.embeddings_dict["ports"]
        )

        # Setup terminal embeddings
        # Since retrieving terminal attributes requires calling TMS' api to extract terminals by each port,
        # we only do it for new ports.
        prev_port_ids, _ = self.embeddings_dict["ports"]
        added_port_ids = [port for port in ports if port not in prev_port_ids]
        if added_port_ids:
            terminal_ids, terminal_embeddings = setup_terminal_embeddings(
                self.bucket, self.embed_model, added_port_ids
            )
        else:
            terminal_ids, terminal_embeddings = self.embeddings_dict["terminals"]

        depot_names, depot_embeddings = setup_depot_embeddings(
            self.bucket, self.embed_model, *self.embeddings_dict["depots"]
        )

        self.embeddings_dict = {
            "container_types": (container_types, container_type_embeddings),
            "ports": (ports, port_embeddings),
            "terminals": (terminal_ids, terminal_embeddings),
            "depots": (depot_names, depot_embeddings),
        }
        return self.embeddings_dict


def setup_embed_model():
    """
    Set up and return a text embedding model.

    Returns:
        TextEmbeddingModel: The initialized text embedding model.
    """
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    return model


def convert_container_number(container_number):
    """
    Convert a container number to ISO standard.

    Args:
        container_number (str): The container number to be converted.

    Returns:
        str: The formatted container number if it is valid, None otherwise.
    """
    if not container_number:
        return
    # 'FFAU2932130--FX34650895-40HC' -> 'FFAU2932130'
    match = re.findall(r"[A-Z]{4}\d{7}", container_number)
    stripped_value = match[0] if match else None

    if not stripped_value:
        stripped_value = "".join(
            filter(lambda char: str.isalnum(char) or char == "/", container_number)
        )

    # This is to catch container number that has the format like: ABCD1234567/40DC or ABCD1234567/SEAL1234567
    formatted_value = stripped_value.split("/")[0]
    if len(formatted_value) != 11:
        return
    # Check if the format is according to the ISO standard
    if not formatted_value[:4].isalpha() or not formatted_value[4:].isdigit():
        return
    return formatted_value


# Clean the date for date obj parse in tms formatting
def clean_date_string(date_str):
    """Remove hours and timezone information from the date string."""
    date_str = date_str.strip()
    if "hrs" in date_str:
        return date_str.replace("hrs", "")
    if "(CET)" in date_str:
        return date_str.replace("(CET)", "")
    return date_str


def extract_date(date_str):
    """
    Extract date from string using european format (day first).

    Check if starts with year, then YYYY-MM-DD, else DD-MM-YYYY
    """
    if all([c.isnumeric() for c in date_str[:4]]):
        dt_obj = pd.to_datetime(date_str, dayfirst=False).to_pydatetime()
    else:
        dt_obj = pd.to_datetime(date_str, dayfirst=True).to_pydatetime()
    return dt_obj


def extract_number(data_field_value):
    """
    Remove everything not a digit and not in [, .].

    Args:
        data_field_value: string

    Returns:
        formatted_value: string

    """
    formatted_value = ""
    for c in data_field_value:
        if c.isnumeric() or c in [",", "."]:
            formatted_value += c

    # First and last characters should not be  [",", "."]
    formatted_value = formatted_value.strip(",.")

    return formatted_value if formatted_value not in ["''", ""] else None


def extract_string(data_field_value):
    """Remove numeric characters from the string.

    Args:
        data_field_value: string

    Returns:
        formatted_value: string

    """
    if not isinstance(data_field_value, str):
        return None

    excluded_chars = [".", ",", ")", "(", " ", "[", "]"]
    formatted_value = "".join(
        c for c in data_field_value if not c.isdigit() and c not in excluded_chars
    )

    return formatted_value if formatted_value not in ["''", ""] else None


def _find_most_similar_option(model, input_string, option_ids, option_embeddings):
    """
    Find the most similar option to the given input string based on embeddings.

    Args:
        model: The model used for generating embeddings.
        input_string (str): The input string to find the most similar option for.
        option_ids (list): The list of option IDs.
        option_embeddings (np.ndarray): The embeddings of the options.

    Returns:
        The ID of the most similar option.
    """
    try:
        input_embedding = model.get_embeddings([input_string])[0].values
        similarities = np.dot(option_embeddings, input_embedding)
        idx = np.argmax(similarities)
        return option_ids[idx]
    except Exception as e:
        logger.error(f"Embeddings error: {e}")
        return None


def extract_google_embed_resp(prediction_string):
    """
    Extract relevant information from the Google Embed API response.

    Args:
        prediction_string (str): The prediction string returned by the Google Embed API.

    Returns:
        dict: A dictionary containing the extracted information.
            - _id (str): The title of the instance.
            - attr_text (str): The content of the instance.
            - embedding (list): The embeddings values from the predictions.

    """
    res = json.loads(prediction_string)
    return dict(
        _id=res["instance"]["title"],
        attr_text=res["instance"]["content"],
        embedding=res["predictions"][0]["embeddings"]["values"],
    )


def load_embed_by_data_field(bucket, embedding_path):
    """
    Load embeddings by data field from the specified bucket and embedding path.

    Args:
        bucket (Bucket): The bucket object representing the storage bucket.
        embedding_path (str): The path to the embeddings in the bucket (different by data_field).

    Returns:
        tuple: A tuple containing the option IDs and option embeddings.
            - option_ids (list): A list of option IDs.
            - option_embeddings (ndarray): An array of option embeddings.
    """
    # Retrieve the embeddings from the output files
    blobs = bucket.list_blobs(prefix=embedding_path)
    all_blob_data = []
    for blob in blobs:
        blob_data = blob.download_as_bytes().decode("utf-8").splitlines()
        embeddings = [extract_google_embed_resp(data) for data in blob_data]
        all_blob_data.extend(embeddings)
    option_ids = [embed["_id"] for embed in all_blob_data]
    option_embeddings = np.array([embed["embedding"] for embed in all_blob_data])
    return option_ids, option_embeddings


def batch_embed(bucket, model, option_strings, suffix):
    """
    Compute embeddings for a batch of option strings and uploads them to a cloud storage bucket.

    Args:
        bucket (google.cloud.storage.bucket.Bucket): The cloud storage bucket to upload the option strings.
        model (SomeModelClass): The model used for computing embeddings.
        option_strings (list): A list of option strings to compute embeddings for.
        suffix (str): A suffix to be used in the storage path for the embeddings.

    Returns:
        tuple: A tuple containing the option IDs and embeddings.
    """
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    input_path = f"embeddings/{suffix}/input/{now}.jsonl"
    blob = bucket.blob(input_path)

    # Convert each dictionary to a JSON string and join them with newlines
    option_strings = [
        {**option, "task_type": "SEMANTIC_SIMILARITY"} for option in option_strings
    ]
    jsonl_string = "\n".join(json.dumps(d) for d in option_strings)

    # Convert the combined string to bytes
    jsonl_bytes = jsonl_string.encode("utf-8")

    # Upload the bytes to the blob
    blob.upload_from_string(jsonl_bytes, content_type="text/plain")

    # Compute embeddings for the options
    embedding_path = f"embeddings/{suffix}/output"
    batch_resp = model.batch_predict(
        dataset=f"gs://{bucket.name}/{input_path}",  # noqa
        destination_uri_prefix=f"gs://{bucket.name}/{embedding_path}",  # noqa
    )

    if batch_resp.state.name != "JOB_STATE_SUCCEEDED":
        logger.warning(
            f"Batch prediction job failed with state {batch_resp.state.name}"
        )
    else:
        logger.info(f"Embeddings for {suffix} computed successfully.")

    option_ids, option_embeddings = load_embed_by_data_field(bucket, embedding_path)
    return option_ids, option_embeddings


def setup_container_type_embeddings(
    bucket, model, computed_container_type_ids, computed_container_type_embeddings
):
    """
    Set up container type embeddings.

    Args:
        bucket (str): The bucket to store the embeddings.
        model: The model used for computing embeddings.
        computed_container_type_ids (list): The list of already computed container type IDs.
        computed_container_type_embeddings (list): The list of already computed container type embeddings.

    Returns:
        tuple: A tuple containing the updated container type IDs and embeddings.
    """
    url = f"https://tms.forto.{tms_domain}/api/transport-units/api/types/list"  # noqa
    resp = call_tms(requests.get, url)
    container_types = resp.json()

    container_attribute_strings = [
        dict(
            title=container_type["code"],
            content=" | ".join(
                ["container type"]
                + [
                    f"{k}: {v}"
                    for k, v in container_type["containerAttributes"].items()
                    if k in ["isoSizeType", "isoTypeGroup"]
                ]
                + [container_type[k] for k in ["displayName", "notes"]]
            ),
        )
        for container_type in container_types
        if container_type["isActive"]
        and container_type["code"] not in computed_container_type_ids
    ]
    if not container_attribute_strings:
        logger.info("No new container types found.")
        return computed_container_type_ids, computed_container_type_embeddings

    logger.info("Computing embeddings for container types...")
    container_type_ids, container_type_embeddings = batch_embed(
        bucket, model, container_attribute_strings, "container_types"
    )
    return container_type_ids, container_type_embeddings


def setup_ports_embeddings(bucket, model, computed_port_ids, computed_port_embeddings):
    """
    Set up port embeddings.

    Steps:
    - Retrieve active ports from the TMS API
    - Compute embeddings for new tradelane-enabled ports
    - Return ALL port IDs and embeddings.

    Args:
        bucket (str): The bucket to store the embeddings.
        model: The model used for computing embeddings.
        computed_port_ids (list): The list of previously computed port IDs.
        computed_port_embeddings (list): The list of previously computed port embeddings.

    Returns:
        tuple: A tuple containing ALL port IDs and embeddings.
    """
    url = f"https://tms.forto.{tms_domain}/api/transport-network/api/ports?pageSize=1000000&status=active"  # noqa
    resp = call_tms(requests.get, url)
    resp_json = resp.json()
    if len(resp_json["data"]) != resp_json["_paging"]["totalRecords"]:
        logger.error("Not all ports were returned.")

    tradelane_enabled_ports = [
        port
        for port in resp_json["data"]
        if "TradeLaneEnabled" in port.get("attributes", [])
        and "tradeLaneRegion" in port
        and port["id"] not in computed_port_ids
    ]
    if not tradelane_enabled_ports:
        logger.info("No new ports found.")
        return computed_port_ids, computed_port_embeddings

    port_attribute_strings = [
        dict(
            title=port["id"],
            content=" | ".join(
                ["port"]
                + [
                    f"{k}-{v}"
                    for k, v in port.items()
                    if k in ["id", "displayName", "countryCode"]
                ]
            ),
        )
        for port in tradelane_enabled_ports
    ]

    logger.info("Computing embeddings for ports.")
    port_ids, port_embeddings = batch_embed(
        bucket, model, port_attribute_strings, "ports"
    )
    return port_ids, port_embeddings


def setup_depot_embeddings(
    bucket, model, computed_depot_names, computed_depot_embeddings
):
    """
    Set up depot embeddings.

    Steps:
    - Retrieve active depot from the TMS API
    - Compute embeddings for new tdepot
    - Return ALL depot names and embeddings.

    Args:
        bucket (str): The bucket to store the embeddings.
        model: The model used for computing embeddings.
        computed_depot_names (list): The list of previously computed depot names.
        computed_depot_embeddings (list): The list of previously computed depot embeddings.

    Returns:
        tuple: A tuple containing ALL depot names and embeddings.
    """
    url = f"https://tms.forto.{tms_domain}/api/transport-network/api/depots?pageSize=1000000"  # noqa
    resp = call_tms(requests.get, url)
    resp_json = resp.json()

    new_depots = [
        depot
        for depot in resp_json["data"]
        if depot["name"] not in computed_depot_names
    ]
    if not new_depots:
        logger.info("No new depots found.")
        return computed_depot_names, computed_depot_embeddings

    depot_attribute_strings = [
        dict(
            title=depot["name"],
            content=" | ".join(
                [
                    "depot",
                    "name - " + depot["name"],
                    "address - " + depot["address"]["fullAddress"],
                ]
            ),
        )
        for depot in resp_json["data"]
    ]

    logger.info("Computing embeddings for depots.")
    depot_names, depot_embeddings = batch_embed(
        bucket, model, depot_attribute_strings, "depots"
    )
    return depot_names, depot_embeddings


def setup_terminal_attributes(port_id: str):
    """
    Retrieve and format the attributes of active terminals at a given port.

    Args:
        port_id (str): The ID of the port.

    Returns:
        list: A list of dictionaries containing the formatted attributes of active terminals.
              Each dictionary has the following keys:
              - title: The terminal's short code.
              - content: A string representation of the terminal's attributes, including its name,
                         searchable name, and full address.
    """
    url = f"https://gateway.forto.{tms_domain}/api/transport-network/api/ports/{port_id}/terminals/list"  # noqa
    resp = call_tms(requests.get, url)
    terminals = resp.json()
    if len(terminals) == 0:
        return []
    active_terminals = [
        term for term in terminals if term["isActive"] & term["isVerified"]
    ]
    if len(active_terminals) == 0:
        logger.warning(f"No active terminals found at port {port_id}.")
        return []

    terminal_attibute_strings = [
        dict(
            title=term["name"],
            content=term["terminalShortCode"]
            + str(
                " | ".join(
                    ["terminal"]
                    + [
                        f"{k}-{v}"
                        for k, v in term.items()
                        if k in ["name", "searchableName"]
                    ]
                )
                + " "
                + term["address"]["fullAddress"],
            ),
        )
        for term in active_terminals
    ]
    return terminal_attibute_strings


def setup_terminal_embeddings(bucket, model, added_port_ids):
    """
    Set up terminal embeddings for `added_port_ids`, using `model`, uploaded to `bucket`.

    Args:
        bucket (str): The bucket to set up terminal embeddings for.
        model (str): The model to use for embedding.
        added_port_ids (list): A list of added port IDs.

    Returns:
        tuple: A tuple containing the ALL terminal IDs and terminal embeddings.
        Not just for the added port IDs.
    """
    terminal_attibute_strings = [
        setup_terminal_attributes(port_id) for port_id in added_port_ids
    ]
    terminal_attibute_strings = sum(terminal_attibute_strings, [])
    if not terminal_attibute_strings:
        logger.info("No new terminals found.")
        return [], np.array([])

    terminal_ids, terminal_embeddings = batch_embed(
        bucket, model, terminal_attibute_strings, "terminals"
    )
    return terminal_ids, terminal_embeddings


def remove_none_values(d):
    if isinstance(d, dict):
        # Create a new dictionary to store non-None values
        cleaned_dict = {}
        for key, value in d.items():
            cleaned_value = remove_none_values(value)
            if cleaned_value is not None:  # Only add non-None values
                cleaned_dict[key] = cleaned_value
        return cleaned_dict if cleaned_dict else None

    elif isinstance(d, list):
        # Create a new list to store non-None values
        cleaned_list = []
        for item in d:
            cleaned_item = remove_none_values(item)
            if cleaned_item is not None:  # Only add non-None values
                cleaned_list.append(cleaned_item)
        return cleaned_list if cleaned_list else None

    else:
        # Return the value if it's not a dictionary or list
        return d if d is not None else None


def check_formatting_rule(entity_key, document_type_code, rule):
    if (
        document_type_code in formatting_rules.keys()
        and entity_key in formatting_rules[document_type_code].keys()
        and formatting_rules[document_type_code][entity_key] == rule
    ):
        return True
    return False


async def format_label(
    entity_k, entity_value, embed_manager, document_type_code, llm_client
):
    if isinstance(entity_value, dict):  # if it's a nested entity
        format_tasks = [
            format_label(sub_k, sub_v, embed_manager, document_type_code, llm_client)
            for sub_k, sub_v in entity_value.items()
        ]
        return entity_k, {k: v for k, v in await asyncio.gather(*format_tasks)}
    if isinstance(entity_value, list):
        format_tasks = await asyncio.gather(
            *[
                format_label(
                    entity_k, sub_v, embed_manager, document_type_code, llm_client
                )
                for sub_v in entity_value
            ]
        )
        return entity_k, [v for _, v in format_tasks]
    entity_key = entity_k.lower()
    embed_model = embed_manager.embed_model
    embeddings_dict = embed_manager.embeddings_dict
    formatted_value = None
    if entity_key.startswith("port"):
        formatted_value = await get_port_code_ai(entity_value, llm_client)
    elif entity_key == "containertype":
        formatted_value = _find_most_similar_option(
            embed_model,
            "container type " + entity_value,
            *embeddings_dict["container_types"],
        )
    elif check_formatting_rule(entity_k, document_type_code, "terminal"):
        formatted_value = _find_most_similar_option(
            embed_model,
            "terminal " + str(entity_value),
            *embeddings_dict["terminals"],
        )
    elif check_formatting_rule(entity_k, document_type_code, "depot"):
        formatted_value = _find_most_similar_option(
            embed_model,
            "depot " + str(entity_value),
            *embeddings_dict["depots"],
        )
    elif entity_key.startswith(("eta", "etd")):
        try:
            cleaned_data_field_value = clean_date_string(entity_value)
            dt_obj = extract_date(cleaned_data_field_value)
            formatted_value = str(dt_obj.date())
        except ValueError as e:
            logger.info(f"ParserError: {e}")
    elif "cutoff" in entity_key:
        try:
            cleaned_data_field_value = clean_date_string(entity_value)
            dt_obj = extract_date(cleaned_data_field_value)
            if dt_obj.tzinfo is None:
                dt_obj = dt_obj.replace(tzinfo=timezone.utc)
            else:
                dt_obj = dt_obj.astimezone(timezone.utc)
            formatted_value = dt_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        except ValueError as e:
            logger.info(f"ParserError: {e}")
    elif entity_key == "containernumber":
        # Remove all non-alphanumeric characters like ' ', '-', etc.
        formatted_value = convert_container_number(entity_value)
    elif any(
        numeric_indicator in entity_key
        for numeric_indicator in [
            "weight",
            "quantity",
            "value",
            "amount",
        ]
    ):
        formatted_value = extract_number(entity_value)
    elif document_type_code == "finalMbL" and entity_key == "measurements":
        formatted_value = extract_number(entity_value)
    elif any(
        packaging_type in entity_key
        for packaging_type in ["packagingtype", "packagetype", "currency"]
    ):
        # Remove all numeric characters from the string. For example 23CARTONS -> CARTONS
        formatted_value = extract_string(entity_value)

    result = {
        "documentValue": entity_value,
        "formattedValue": formatted_value,
    }
    return entity_k, result


async def get_port_code_ai(port: str, llm_client):
    if (
        "postprocessing" in prompt_library.library.keys()
        and "port_code" in prompt_library.library["postprocessing"].keys()
    ):
        # Get the prompt from the prompt library and prepare the response schema for ChatGPT
        prompt = prompt_library.library["postprocessing"]["port_code"]["prompt"]
        response_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "port",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "port": {
                            "type": "string",
                            "description": f"Get the port code for the given port: {port}",
                        }
                    },
                    "required": ["port"],
                    "additionalProperties": False,
                },
            },
        }

        response = await llm_client.get_unified_json_genai(
            prompt, response_schema=response_schema, model="chatgpt"
        )
        try:
            # TODO: replace hard-coded values with general solution that takes shipment context
            hard_code_port_dict = {
                "CNSHA": "CNSHG",
                "CNNGB": "CNNBG",
                "CNTAO": "CNQDG",
            }
            mapped_port = response["port"]
            return hard_code_port_dict.get(mapped_port, mapped_port)
        except json.JSONDecodeError:
            logger.error(f"Error decoding response: {response}")
            return None


async def format_all_entities(result, embed_manager, document_type_code, llm_client):
    # remove None values from dict
    result = remove_none_values(result)
    if result is None:
        logger.info("No data was extracted.")
        return {}
    _, aggregated_data = await format_label(
        None, result, embed_manager, document_type_code, llm_client
    )

    logger.info("Data Extraction completed successfully")

    return aggregated_data
