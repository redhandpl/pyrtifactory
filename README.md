# Artifactory REST API wrapper

| WARNING: This is the very first alpha release. |
| --- |

| INFO: This code is written for Python 3. |
| --- |

## How to install?
```bash
python3 setup.py install --user
```

## Examples
```python
import pyrtifactory

results = pyrtifactory.artifactoryAPI(
    url='https://artifactory.domain.tld/artifactory',
    username='USER',
    password='PASSWORD'
    )

repositories = results.getRepositories(params = {'type': 'local', 'packageType': 'docker'})
print(repositories)
```


## Wrapper
artifactoryWrapper.py - Try it!
