from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import responses
from responses import matchers

from codecov_cli.services.staticanalysis import run_analysis_entrypoint
from codecov_cli.services.staticanalysis.types import FileAnalysisRequest


class TestStaticAnalysisService:
    @pytest.mark.asyncio
    @patch("codecov_cli.services.staticanalysis.select_file_finder")
    @patch("codecov_cli.services.staticanalysis.send_single_upload_put")
    async def test_static_analysis_service(
        self, mock_send_upload_put, mock_file_finder
    ):
        files_found = map(
            lambda filename: FileAnalysisRequest(str(filename), Path(filename)),
            [
                "samples/inputs/sample_001.py",
                "samples/inputs/sample_002.py",
            ],
        )
        mock_file_finder.return_value.find_files = MagicMock(return_value=files_found)
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "https://api.codecov.io/staticanalysis/analyses",
                json={
                    "filepaths": [
                        {
                            "state": "created",
                            "filepath": "samples/inputs/sample_001.py",
                            "raw_upload_location": "some URL",
                        },
                        {
                            "state": "valid",
                            "filepath": "samples/inputs/sample_002.py",
                            "raw_upload_location": "some URL",
                        },
                    ]
                },
                status=200,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            await run_analysis_entrypoint(
                config={},
                folder=".",
                numberprocesses=1,
                pattern="*.py",
                token="STATIC_TOKEN",
                commit="COMMIT",
                should_force=False,
                folders_to_exclude=[],
            )
        mock_file_finder.assert_called_with({})
        mock_file_finder.return_value.find_files.assert_called()
        assert mock_send_upload_put.call_count == 1
        args, _ = mock_send_upload_put.call_args
        assert args[2] == {
            "state": "created",
            "filepath": "samples/inputs/sample_001.py",
            "raw_upload_location": "some URL",
        }

    @pytest.mark.asyncio
    @patch("codecov_cli.services.staticanalysis.select_file_finder")
    @patch("codecov_cli.services.staticanalysis.send_single_upload_put")
    async def test_static_analysis_service_should_force_option(
        self, mock_send_upload_put, mock_file_finder
    ):
        files_found = map(
            lambda filename: FileAnalysisRequest(str(filename), Path(filename)),
            [
                "samples/inputs/sample_001.py",
                "samples/inputs/sample_002.py",
            ],
        )
        mock_file_finder.return_value.find_files = MagicMock(return_value=files_found)
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "https://api.codecov.io/staticanalysis/analyses",
                json={
                    "filepaths": [
                        {
                            "state": "created",
                            "filepath": "samples/inputs/sample_001.py",
                            "raw_upload_location": "some URL",
                        },
                        {
                            "state": "valid",
                            "filepath": "samples/inputs/sample_002.py",
                            "raw_upload_location": "some URL",
                        },
                    ]
                },
                status=200,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            await run_analysis_entrypoint(
                config={},
                folder=".",
                numberprocesses=1,
                pattern="*.py",
                token="STATIC_TOKEN",
                commit="COMMIT",
                should_force=True,
                folders_to_exclude=[],
            )
        mock_file_finder.assert_called_with({})
        mock_file_finder.return_value.find_files.assert_called()
        assert mock_send_upload_put.call_count == 2
        args, _ = mock_send_upload_put.call_args
