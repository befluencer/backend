import uuid, os
from dreema.helpers import getconfig
from dreema.helpers import Json


class FileParser:

    async def getMultipartKeys(self, parser: bytes):
        partObj = {}
        for d in parser:
            if not d.get("contenttype", None):
                partObj[d["name"]] = (
                    d["content"].strip().strip(b'"').decode().replace("\r\n", "")
                )
            else:
                content = d["contenttype"]
                ext = content.split("/")[1]
                tempUploadDir = "storage/temp"
                os.makedirs(tempUploadDir, exist_ok=True)

                uniquename = uuid.uuid4().hex
                path = os.path.join(tempUploadDir, f"{uniquename}.{ext}")

                # Save the file
                with open(path, "wb") as f:
                    f.write(d["content"])

                partObj[d["name"]] = (
                    Json(
                        {
                            "type": content,
                            "ext": ext,
                            "fullPath": path,
                            "size": len(d["content"]),
                        }
                    )
                )

                # save the content to a temporary file location
        return partObj

    async def parseMultipart(self, body: bytes, content: bytes):
        boundary = content.split("boundary=")[-1].strip().encode()

        # Split the body by boundary delimiter
        parts = body.split(b"--" + boundary)
        parts = [part for part in parts if part and part != b"--\r\n" and part != b"--"]

        data = []
        for part in parts:
            header, content = part.split(b"\r\n\r\n", 1)
            headers = {}
            # Step 1: Normalize line endings and split into individual header lines
            lines = header.strip().replace(b"\r\n", b"\n").split(b"\n")
            headers = {}
            for line in lines:
                if b":" in line:
                    # column type key names
                    key, value = line.split(b":", 1)
                    key = (
                        key.strip().decode().lower().replace("-", "")
                    )  # e.g. 'content-disposition'

                    # equal to type key names
                    parts = [p.strip() for p in value.split(b";")]
                    headers[key] = parts[0].decode()
                    for part in parts[1:]:
                        if b"=" in part:
                            subkey, subval = part.split(b"=", 1)
                            subkey = subkey.strip().decode().lower()
                            subval = (
                                subval.strip().strip(b'"').decode().replace("\r\n", "")
                            )

                            headers[subkey] = subval

            # append content
            headers["content"] = content
            data.append(headers)

        return data
