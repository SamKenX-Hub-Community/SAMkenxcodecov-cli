from codecov_cli.helpers.ci_adapters import (
    AppveyorCIAdapter,
    AzurePipelinesCIAdapter,
    BuildkiteAdapter,
    CircleCICIAdapter,
    CirrusCIAdapter,
    DroneCIAdapter,
    GithubActionsCIAdapter,
    GitlabCIAdapter,
    HerokuCIAdapter,
    JenkinsAdapter,
    LocalAdapter,
    WoodpeckerCIAdapter,
    get_ci_adapter,
)


class TestCISelector(object):
    def test_returns_none_if_name_is_invalid(self):
        assert get_ci_adapter("random ci adapter name") is None

    def test_returns_circleCI(self):
        assert isinstance(get_ci_adapter("circleci"), CircleCICIAdapter)

    def test_returns_githubactions(self):
        assert isinstance(get_ci_adapter("githubactions"), GithubActionsCIAdapter)

    def test_returns_gitlabCI(self):
        assert isinstance(get_ci_adapter("gitlabCI"), GitlabCIAdapter)

    def test_returns_appveyor(self):
        assert isinstance(get_ci_adapter("appveyor"), AppveyorCIAdapter)

    def test_returns_local(self):
        assert isinstance(get_ci_adapter("local"), LocalAdapter)

    def test_returns_woodpecker(self):
        assert isinstance(get_ci_adapter("woodpecker"), WoodpeckerCIAdapter)

    def test_returns_herokuci(self):
        assert isinstance(get_ci_adapter("heroku"), HerokuCIAdapter)

    def test_returns_droneci(self):
        assert isinstance(get_ci_adapter("droneci"), DroneCIAdapter)

    def test_returns_buildkite(self):
        assert isinstance(get_ci_adapter("buildkite"), BuildkiteAdapter)

    def test_returns_azurepipelines(self):
        assert isinstance(get_ci_adapter("azurepipelines"), AzurePipelinesCIAdapter)

    def test_returns_jenkins(self):
        assert isinstance(get_ci_adapter("jenkins"), JenkinsAdapter)

    def test_returns_cirrusci(self):
        assert isinstance(get_ci_adapter("cirrusci"), CirrusCIAdapter)
