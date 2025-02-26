import asyncio

import aiofiles
import httpx
from urllib.parse import urlencode
from ..models import ErrorReport, File, CopyModel, MultipartWrapper, PartInfo
from typing import Union
from ..utils import safe_data_request

endpoint = "file"
#
# def initialize_upload(baseurl: str, file: File, token: str) -> Union[File, ErrorReport]:
#     uri = baseurl + endpoint
#     data = file.model_dump_json(by_alias=True, exclude_none=True)
#     head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}', 'total': f'{file.total}'}
#
#     response = safe_data_request('POST', uri, data, head)
#     if isinstance(response, ErrorReport):
#         return response
#     return File.model_validate(response)
#
# def send_part(baseurl: str, part_raw: bytes, index: int, file_id, token: str) -> Union[File, ErrorReport]:
#     uri = baseurl + f'{endpoint}/{file_id}?part={index}'
#     headers = {'Content-Type': 'application/octet-stream', 'Authorization': f'Bearer {token}', 'Content-Length': f'{len(part_raw)}'}
#     response = safe_data_request('POST', uri, headers=headers, data=part_raw)
#     if isinstance(response, ErrorReport):
#         raise ValueError(f"HTTP Status: {response.status} \nHTTP Reason: {response.reason} \nAPI Message: {response.message} \nAPI Status Code: {response.internal_status}")
#     return File.model_validate(response)
#
#
# async def async_send_part(baseurl: str, part_raw: bytes, index: int, file_id: str, token: str, semaphore: asyncio.Semaphore, client: httpx.AsyncClient) -> Union[File, ErrorReport]:
#     """Asynchronously send a file part to the API with limited concurrency."""
#     uri = f"{baseurl}{endpoint}/{file_id}?part={index}"
#     headers = {
#         "Content-Type": "application/octet-stream",
#         "Authorization": f"Bearer {token}",
#         "Content-Length": str(len(part_raw)),
#     }
#
#     async with semaphore:  # Limit concurrency
#         try:
#             response = await client.post(uri, headers=headers, content=part_raw, timeout=120.0)
#             if response.status_code >= 300:
#                 raise ValueError(f"Chunk {index} failed with HTTP {response.status_code}: {response.text}")
#             return File.model_validate(response.json())
#
#         except httpx.ReadTimeout:
#             print(f"Chunk {index} ReadTimeout. Retrying...")
#             return await async_send_part(baseurl, part_raw, index, file_id, token, semaphore, client)  # Retry request

async def upload_part(part: PartInfo, chunk: bytes, concurrent_sessions: int, chunk_size: int, progress_bar):
    semaphore = asyncio.Semaphore(concurrent_sessions)

    async with semaphore:  # ✅ Limit concurrent uploads
        part_number = part.number
        url = part.presigned_url

        # async with aiofiles.open(path, "rb") as f:
        #     await f.seek((part_number - 1) * chunk_size)
        #     chunk = await f.read(chunk_size)
        #
        # if not chunk:
        #     part.uploaded = False
        #     raise EOFError(f'Could not read chunk with number {part_number}')

        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.put(url, content=chunk, headers={"Content-Type": "application/octet-stream"})
        if response.status_code == 200:
            etag = response.headers.get("ETag", "").strip('"')
            part.etag = etag
            part.uploaded = True

            # Upload logic here...
            progress_bar.update(1)  # ✅ Update progress after each part upload

        else:
            part.uploaded = False
            print(f"❌ Failed to upload part {part_number}: {response.text}")


async def initiate_upload(baseurl: str, file: File, size: int, chunk_size: int, token: str) -> Union[MultipartWrapper, ErrorReport]:
    headers = {'Authorization': f'Bearer {token}', 'File-Size':str(size), 'Chunk-Size':str(chunk_size), 'Content-Type': 'application/json'}
    url = f"{baseurl}file/upload/initialize"
    data = file.model_dump_json(by_alias=True, exclude_none=True)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        try:
            response = MultipartWrapper.model_validate(response.json())
        except:
            response = ErrorReport.model_validate(response.json())
        return response

async def close_multipart(baseurl: str, parts: MultipartWrapper, token: str) -> Union[File, ErrorReport]:
    url = f"{baseurl}file/upload/complete"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = parts.model_dump_json(by_alias=True, exclude_none=True)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        try:
            response = File.model_validate(response.json())
        except:
            response = ErrorReport.model_validate(response.json())
        return response


async def initiate_download(baseurl: str, file_id: str, token: str) -> Union[MultipartWrapper, ErrorReport]:
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    url = f"{baseurl}file/download/initialize/{file_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        try:
            response = MultipartWrapper.model_validate(response.json())
        except:
            response = ErrorReport.model_validate(response.json())
        return response

async def download_part(presigned_url, concurrent_sessions, progress_bar):
    semaphore = asyncio.Semaphore(concurrent_sessions)

    async with semaphore:  # ✅ Limit concurrent uploads
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.get(presigned_url, headers={"Content-Type": "application/octet-stream"})

        if response.status_code == 200:
            progress_bar.update(1)
        else:
            print(f"❌ Failed to download chunk part with URL {presigned_url}")
        return response.content


def beta_send_part(baseurl: str, part_raw: bytes, index: int, file_id, token: str) -> Union[File, ErrorReport]:
    import httpx

    uri = baseurl + f'{endpoint}/{file_id}?part={index}'
    headers = {'Content-Type': 'application/octet-stream', 'Authorization': f'Bearer {token}', 'Content-Length': f'{len(part_raw)}'}
    response = httpx.post(uri, headers=headers, content=part_raw, timeout=60.0)
    if isinstance(response, ErrorReport):
        raise ValueError(f"HTTP Status: {response.status} \nHTTP Reason: {response.reason} \nAPI Message: {response.message} \nAPI Status Code: {response.internal_status}")
    return File.model_validate(response.json())

def get_part(baseurl: str, file_id: str, results: list, index: int, token: str):
    uri = baseurl + f'{endpoint}/{file_id}?part={index}'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('GET', uri, headers=headers, data=None)
    if isinstance(response, ErrorReport):
        return response

    results[index-1] = response

def get_info(baseurl: str, file_id: str, token: str) -> Union[File, ErrorReport]:
    uri = baseurl + f'{endpoint}/info/{file_id}'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('GET', uri, headers=headers, data=None)
    if isinstance(response, ErrorReport):
        return response
    return File.model_validate(response)

def delete_file(baseurl: str, file_id: str, token: str) -> Union[File, ErrorReport]:
    uri = baseurl + endpoint + f'/{file_id}'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('DELETE', uri, None, headers)
    if isinstance(response, ErrorReport):
        return response
    return None

def update_file(baseurl: str, body: File, token: str) -> Union[File, ErrorReport]:
    data = body.model_dump_json(by_alias=True)
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    uri = baseurl + endpoint

    response = safe_data_request('PUT', uri, data, head)
    if isinstance(response, ErrorReport):
        return response
    return File.model_validate(response)


def copy_file(baseurl: str, body: CopyModel, token: str) -> Union[File, ErrorReport]:
    uri = baseurl + endpoint + '/copy'
    data = body.model_dump_json(by_alias=True)
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('POST', uri, data, head)
    if isinstance(response, ErrorReport):
        return response
    return File.model_validate(response)


def move_file(baseurl: str, body: CopyModel, token: str) -> Union[File, ErrorReport]:
    uri = baseurl + endpoint + '/move'
    data = body.model_dump_json(by_alias=True)
    head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    response = safe_data_request('PUT', uri, data, head)
    if isinstance(response, ErrorReport):
        return response
    return File.model_validate(response)