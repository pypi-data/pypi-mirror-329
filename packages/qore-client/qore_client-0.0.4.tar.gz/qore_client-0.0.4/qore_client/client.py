from typing import Any, Dict, List, Optional, Union

import requests
from requests import Response


class QoreClient:
    """
    Qore API Client
    ~~~~~~~~~~~~~~~

    Qore 서비스에 접근할 수 있는 파이썬 Client SDK 예시입니다.
    """

    BASE_URL = "https://api-qore.quantit.io"

    def __init__(self, api_key: str) -> None:
        """
        :param api_key: Qore API 인증에 사용되는 Bearer 토큰
        """
        self.api_key = api_key

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], List[tuple]]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        내부적으로 사용하는 공통 요청 메서드

        :param method: HTTP 메서드 (GET, POST, PATCH, DELETE 등)
        :param path:   API 엔드포인트 경로 (ex: "/d/12345")
        :param params: query string으로 전송할 딕셔너리
        :param data:   폼데이터(form-data) 등으로 전송할 딕셔너리
        :param json:   JSON 형태로 전송할 딕셔너리
        :param files:  multipart/form-data 요청 시 사용할 파일(dict)
        :return:       응답 JSON(dict) 또는 raw 데이터
        """
        url = f"{self.BASE_URL}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        response: Response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            files=files,
            headers=headers,
        )
        # 에러 발생 시 raise_for_status()가 예외를 던짐
        response.raise_for_status()

        # 일부 DELETE 요청은 204(No Content)일 수 있으므로, 이 경우 JSON 파싱 불가
        if response.status_code == 204 or not response.content:
            return None

        return response.json()

    # ----------------------------------------------------------------------------
    # 1. 서버 상태 조회 ( GET / )
    # ----------------------------------------------------------------------------
    def get_server_status(self) -> Dict[str, Any]:
        """
        서버 상태 조회

        :return: {
          "success": "서버 상태 문자열",
          "version": "버전 문자열",
          "env": "서버 환경"
        }
        """
        return self._request("GET", "/")

    # ----------------------------------------------------------------------------
    # 2. Drive 관련
    # ----------------------------------------------------------------------------
    def get_drive(self, drive_id: str) -> Dict[str, Any]:
        """
        Drive 상세 조회

        :param drive_id: 조회할 Drive의 ID
        :return: Drive 정보
        """
        return self._request("GET", f"/d/{drive_id}")

    def create_drive(self, org_id: str, name: str) -> Dict[str, Any]:
        """
        조직 내에 Drive 생성

        :param org_id:  조직 ID
        :param name:    생성할 드라이브 이름
        :return: 생성된 드라이브의 정보
        """
        payload = {"name": name}
        return self._request("POST", f"/o/{org_id}/d/create", json=payload)

    def list_drives(self, org_id: str) -> List[Dict[str, Any]]:
        """
        조직 내의 Drive 목록 조회

        :param org_id: 조직 ID
        :return: Drive 목록
        """
        return self._request("GET", f"/o/{org_id}/d/list")

    def update_drive(self, drive_id: str, name: str) -> Dict[str, Any]:
        """
        Drive 이름 수정 (부분 업데이트, PATCH)

        :param drive_id: 수정할 Drive ID
        :param name:     수정된 Drive 이름
        :return: 수정된 Drive의 정보
        """
        payload = {"name": name}
        return self._request("PATCH", f"/d/{drive_id}/update", json=payload)

    def delete_drive(self, drive_id: str) -> None:
        """
        Drive 삭제

        :param drive_id: 삭제할 Drive ID
        """
        self._request("DELETE", f"/d/{drive_id}/delete")

    # ----------------------------------------------------------------------------
    # 3. File 관련
    # ----------------------------------------------------------------------------
    def create_file(self, folder_id: str, file_path: str) -> Dict[str, Any]:
        """
        파일 생성 (multipart/form-data)

        :param folder_id: 업로드 대상 폴더의 ID
        :param file_path: 업로드할 파일 경로
        :return: 생성된 파일 정보
        """
        # files: {"file": (filename, fileobject, content_type)}
        # 간단하게 할 경우 content_type은 생략 가능
        files = {"file": open(file_path, "rb")}
        data = {"folder_id": folder_id}
        return self._request("POST", "/file/create", data=data, files=files)

    def get_file(self, file_id: str) -> Dict[str, Any]:
        """
        파일 조회

        :param file_id: 조회할 파일의 ID
        :return: 파일 정보 (id, name, size, mime_type 등)
        """
        return self._request("GET", f"/file/{file_id}")

    def delete_file(self, file_id: str) -> None:
        """
        파일 삭제

        :param file_id: 삭제할 파일 ID
        """
        self._request("DELETE", f"/file/{file_id}/delete")

    # ----------------------------------------------------------------------------
    # 4. Folder 관련
    # ----------------------------------------------------------------------------
    def create_folder(
        self, drive_id: str, name: str, parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        폴더 생성

        :param drive_id: 폴더를 생성할 드라이브 ID
        :param name:     생성할 폴더 이름
        :param parent_id: 상위 폴더 ID (없으면 루트 폴더에 생성)
        :return: 생성된 폴더 정보
        """
        payload = {
            "drive_id": drive_id,
            "name": name,
        }
        if parent_id:
            payload["parent_id"] = parent_id

        return self._request("POST", "/folder/create", json=payload)

    def get_folder(self, folder_id: str) -> Dict[str, Any]:
        """
        폴더 조회

        :param folder_id: 조회할 폴더 ID
        :return: 폴더 상세 정보
        """
        return self._request("GET", f"/folder/{folder_id}")

    def update_folder(self, folder_id: str, name: str) -> Dict[str, Any]:
        """
        폴더 이름 수정

        :param folder_id: 수정할 폴더 ID
        :param name:      새로운 폴더 이름
        :return: 수정된 폴더 정보
        """
        payload = {"name": name}
        return self._request("PATCH", f"/folder/{folder_id}/update", json=payload)

    def delete_folder(self, folder_id: str) -> None:
        """
        폴더 삭제

        :param folder_id: 삭제할 폴더 ID
        """
        self._request("DELETE", f"/folder/{folder_id}/delete")

    # ----------------------------------------------------------------------------
    # 5. User 관련
    # ----------------------------------------------------------------------------
    def get_me(self) -> Dict[str, Any]:
        """
        내 정보 조회

        :return: 사용자 정보
        """
        return self._request("GET", "/me")

    # ----------------------------------------------------------------------------
    # 6. Organization(조직) 관련
    # ----------------------------------------------------------------------------
    def create_organization(
        self, name: str, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        조직 생성

        :param name:         조직 이름
        :param description:  조직 설명(옵션)
        :return: 생성된 조직 정보
        """
        payload = {"name": name}
        if description is not None:
            payload["description"] = description

        return self._request("POST", "/o/create", json=payload)

    def list_organizations(self) -> List[Dict[str, Any]]:
        """
        조직 목록 조회
        :return: 조직 목록
        """
        return self._request("GET", "/o/list")

    def get_organization(self, org_id: str) -> Dict[str, Any]:
        """
        조직 상세 조회

        :param org_id: 조회할 조직 ID
        :return: 조직 상세 정보
        """
        return self._request("GET", f"/o/{org_id}")

    def update_organization(
        self, org_id: str, name: Optional[str] = None, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        조직 수정

        :param org_id:      수정할 조직 ID
        :param name:        변경할 조직 이름
        :param description: 변경할 조직 설명
        :return: 수정된 조직 정보
        """
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description

        return self._request("PATCH", f"/o/{org_id}/update", json=payload)

    def delete_organization(self, org_id: str) -> None:
        """
        조직 삭제

        :param org_id: 삭제할 조직 ID
        """
        self._request("DELETE", f"/o/{org_id}/delete")

    # ----------------------------------------------------------------------------
    # 7. Workspace 관련
    # ----------------------------------------------------------------------------
    def create_workspace(
        self, org_id: str, name: str, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        워크스페이스 생성

        :param org_id:      소속될 조직 ID
        :param name:        생성할 워크스페이스 이름
        :param description: 워크스페이스 설명(옵션)
        :return: 생성된 워크스페이스 정보
        """
        payload = {"name": name}
        if description is not None:
            payload["description"] = description

        return self._request("POST", f"/o/{org_id}/w/create", json=payload)

    def list_workspaces(self, org_id: str) -> List[Dict[str, Any]]:
        """
        워크스페이스 목록 조회

        :param org_id: 소속 조직 ID
        :return: 워크스페이스 목록
        """
        return self._request("GET", f"/o/{org_id}/w/list")

    def get_workspace(self, workspace_id: str) -> Dict[str, Any]:
        """
        워크스페이스 상세 조회

        :param workspace_id: 조회할 워크스페이스 ID
        :return: 워크스페이스 상세 정보
        """
        return self._request("GET", f"/w/{workspace_id}")

    def update_workspace(
        self,
        workspace_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        워크스페이스 수정

        :param workspace_id:  수정할 워크스페이스 ID
        :param name:          변경할 이름
        :param description:   변경할 설명
        :return: 수정된 워크스페이스 정보
        """
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description

        return self._request("PATCH", f"/w/{workspace_id}/update", json=payload)

    def delete_workspace(self, workspace_id: str) -> None:
        """
        워크스페이스 삭제

        :param workspace_id: 삭제할 워크스페이스 ID
        """
        self._request("DELETE", f"/w/{workspace_id}/delete")


if __name__ == "__main__":
    client = QoreClient(
        api_key="TEST_TOKEN"
    )

    print(client.list_drives("Organization_ID"))

    print(client.get_drive("Drive_ID"))

    print(client.get_folder("Folder_ID"))

    print(client.get_file("File_ID"))

    
    
