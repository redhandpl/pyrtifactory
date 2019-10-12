# Artifactory REST API wrapper

| WARNING: This is the very first alpha release. |
| --- |

## Examples
```
import pyrtifactory

results = pyrtifactory.artifactoryAPI(
    url='https://artifactory.domain.tld/artifactory',
    username='USER',
    password='PASSWORD'
    )

repositories = results.getRepositories(params = {'type': 'local', 'packageType': 'docker'})
print(repositories)
```
