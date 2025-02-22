# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .account_token import *
from .application import *
from .application_set import *
from .cluster import *
from .project import *
from .project_token import *
from .provider import *
from .repository import *
from .repository_certificate import *
from .repository_credentials import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_argocd.config as __config
    config = __config
else:
    config = _utilities.lazy_import('pulumi_argocd.config')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "argocd",
  "mod": "index/accountToken",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/accountToken:AccountToken": "AccountToken"
  }
 },
 {
  "pkg": "argocd",
  "mod": "index/application",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/application:Application": "Application"
  }
 },
 {
  "pkg": "argocd",
  "mod": "index/applicationSet",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/applicationSet:ApplicationSet": "ApplicationSet"
  }
 },
 {
  "pkg": "argocd",
  "mod": "index/cluster",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/cluster:Cluster": "Cluster"
  }
 },
 {
  "pkg": "argocd",
  "mod": "index/project",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/project:Project": "Project"
  }
 },
 {
  "pkg": "argocd",
  "mod": "index/projectToken",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/projectToken:ProjectToken": "ProjectToken"
  }
 },
 {
  "pkg": "argocd",
  "mod": "index/repository",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/repository:Repository": "Repository"
  }
 },
 {
  "pkg": "argocd",
  "mod": "index/repositoryCertificate",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/repositoryCertificate:RepositoryCertificate": "RepositoryCertificate"
  }
 },
 {
  "pkg": "argocd",
  "mod": "index/repositoryCredentials",
  "fqn": "pulumi_argocd",
  "classes": {
   "argocd:index/repositoryCredentials:RepositoryCredentials": "RepositoryCredentials"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "argocd",
  "token": "pulumi:providers:argocd",
  "fqn": "pulumi_argocd",
  "class": "Provider"
 }
]
"""
)
