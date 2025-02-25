try:
    import os
    import json
    from django.conf import settings
    from drf_spectacular.openapi import AutoSchema as SpectacularAutoSchema
    from collections import OrderedDict
except ImportError:
    raise ImportError("Json Crack AutoSchema requires drf-spectacular and Django.")

# Ensure a directory exists for storing images
folder_code = f"{settings.SECRET_KEY[-10:][::-1]}"
media_dir = os.path.join(settings.MEDIA_ROOT, folder_code)
MEDIA_DIR = os.path.join(settings.BASE_DIR, media_dir)
os.makedirs(MEDIA_DIR, exist_ok=True)
code_mapping_file_path = os.path.join(MEDIA_DIR, "code_mapping.json")
if not os.path.exists(code_mapping_file_path):
    with open(code_mapping_file_path, "w") as f:
        json.dump({}, f)
visualizer_key = "Visualization"

class AutoSchema(SpectacularAutoSchema):
    """
    Custom AutoSchema that replaces application/json responses
    with image/png documentation, embedding a PNG via JsonCrack.
    """

    def get_host_details(self):
        """
        Extract protocol, host, and port from the request object.
        """
        request = getattr(self.view, "request", None)
        if not request:
            return None, None, None  # Fallback if request is not available

        # Determine protocol
        protocol = "https" if request.is_secure() else "http"

        # Get host (includes domain & port)
        full_host = request.get_host()  # Example: "127.0.0.1:8000"

        # Extract separate host and port
        host, _, port = full_host.partition(":")
        if not port:
            port = "443" if protocol == "https" else "80"  # Default ports

        return protocol, host, port

    def _get_response_bodies(self, direction="response"):
        protocol, host, port = self.get_host_details()
        from JsonCrack.Cracker import JSON  # Delay the import to avoid early Django setup issues
        from JsonCrack.fuctions import CodeDictionaryMapper
        mapper = CodeDictionaryMapper(filename=code_mapping_file_path)
        # Let drf-spectacular build the default response bodies
        responses = super()._get_response_bodies(direction=direction)
        try:
            for status_code, openapi_response in list(responses.items()):
                # Check if this response includes 'application/json' docs
                if "content" in openapi_response and "application/json" in openapi_response["content"]:
                    # Grab the schema describing the JSON structure
                    schema_data = openapi_response["content"]["application/json"]["schema"]
                    properties = schema_data.get("properties")
                    if properties:
                        if isinstance(properties, dict):
                            data = {}
                            for key, value in properties.items():

                                if isinstance(value, dict) and key != visualizer_key:
                                    default = value.get("default")
                                    if default:
                                        data[key] = default
                            # Generate a PNG from that example
                            code = mapper.add_entry(data)
                            #data = mapper.get_dict_by_code(code)
                            image_filename = code
                            image_path = os.path.join(MEDIA_DIR, image_filename)
                            if not os.path.exists(os.path.join(MEDIA_DIR, image_filename)):
                            #if not image_filename in os.listdir(MEDIA_DIR):
                                json_obj = JSON(data)
                                json_obj.visualize(output_file=image_path, display=False,silent=True)
                            # Insert key at the beginning
                            #openapi_response["description"] = f"Description:{openapi_response["description"]} | {visualizer_key}: {os.path.join(settings.MEDIA_URL,folder_code,f'{image_filename}.png')}"
                            # Corrected way to add links
                            openapi_response.setdefault("links", {})
                            openapi_response["links"][visualizer_key] = {
                                "operationId": f"{protocol or 'http'}://{host or 'localhost'}:{port or '8000'}{os.path.join(settings.MEDIA_URL,folder_code,f'{image_filename}.png')}",
                                "description": "Visualization of JSON structure",
                            }
                            # schema_data["properties"] = OrderedDict([(visualizer_key, {"default": os.path.join(settings.MEDIA_URL,folder_code,f"{image_filename}.png"),
                            #                             'type': "string"})] + list(properties.items()))
            return responses
        except Exception as e:
            print(e)
            return responses

    def _extract_defaults(self, schema_data):
        """
        Recursively build a dictionary from the schema's 'properties'
        and 'default' fields so we have something to visualize.
        """
        if not schema_data or "properties" not in schema_data:
            return {}

        def build_example(properties):
            result = {}
            for key, val in properties.items():
                if "default" in val:
                    # Use the 'default' field as the example
                    result[key] = val["default"]
                elif val.get("type") == "object" and "properties" in val:
                    # Recursively handle nested objects
                    result[key] = build_example(val["properties"])
                else:
                    # Otherwise just put None or empty as fallback
                    result[key] = None
            return result

        return build_example(schema_data["properties"])

