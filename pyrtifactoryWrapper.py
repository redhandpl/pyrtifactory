#!/usr/bin/env python3

import argparse
import os
import sys
import pyrtifactory

VERSION = "0.1"

artifactoryUrls = ["https://first.instance.tld/artifactory", "https://second.instance.tld/artifactory"]

repositoryClasses = ["local", "virtual", "remote"]
repositoryTypes = ["maven", "gradle", "ivy", "sbt", "helm", "cocoapods", "opkg", "rpm", "nuget", "cran", "gems", "npm", "bower", "debian", "pypi", "docker",
                   "yum", "vcs", "composer", "go", "p2", "chef", "puppet", "generic"]


def parseArgs():
    parser = argparse.ArgumentParser(description="Artifactory CLI v" + VERSION,
                                     epilog="The power of ONG!",
                                     add_help=True)
    parser.add_argument("-v", "--version", action='version', version="%(prog)s " + VERSION)
    parser.add_argument("--debug", help="enable debug mode", action="store_true")

    status = parser.add_argument_group('status')
    status.add_argument("--ping", help="check if Artifactory instances are alive", action="store_true")

    repositories = parser.add_argument_group('repositories', 'Manipulating repositories')
    repositoriesExclusive = repositories.add_mutually_exclusive_group()
    repositoriesExclusive.add_argument('--get-repositories', help="list repositories (JSON) (req: --rclass, --type)", action="store_true")
    repositoriesExclusive.add_argument('--create-repository', help="create a new repository (req: --rclass, --type)", action="store_true")
    repositoriesExclusive.add_argument('--delete-repository', help="delete a repository (req: --name)", action="store_true")
    repositories.add_argument('--name', help="name of the repository", action="store")
    repositories.add_argument('--rclass', help="repository class: local, virtual, remote (default: local)", action="store", default="local")
    repositories.add_argument('--type', help="repository type: maven | gradle | ivy | sbt | helm | cocoapods | opkg | rpm| nuget | cran | \
                                                               gems | npm | bower | debian | pypi | docker | yum | vcs | composer | go | \
                                                               p2 | chef | puppet | generic")
    repositories.add_argument('--instance', help="set Artifactory instance: city_a, city_b, all (default: all)", action="store", default="all")

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    return parser

def testEnvVars():
    try:
        artifactoryUser = os.environ['ARTIFACTORY_USER']
        artifactoryPass = os.environ['ARTIFACTORY_PASS']

        return artifactoryUser, artifactoryPass
    except KeyError as e:
        print("Environment variables are not set: {0}".format(e))
        sys.exit(1)

def connect(instance):
    artifactoryInstance = pyrtifactory.artifactoryAPI(
        url=instance,
        username=artifactoryUser,
        password=artifactoryPass
    )

    return artifactoryInstance

def artifactoryLocation(instance):
    if instance == artifactoryUrls[0]:
        location = "City_A"
    elif instance == artifactoryUrls[1]:
        location = "City_B"

    return location

def setInstance(instance):
    instances = ['None']

    if instance == "city_a":
        instances[0] = artifactoryUrls[0]
    elif instance == "city_b":
        instances[0] = artifactoryUrls[1]
    elif instance == "all":
        instances = artifactoryUrls
    else:
        print("I'm sorry, Dave. I'm afraid I can't do that.\nI don't know the instance \"" + args.instance + "\".")
        sys.exit(78)

    return instances


if __name__ == '__main__':
    args = parseArgs().parse_args()
    artifactoryUser, artifactoryPass = testEnvVars()

    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    artifactoryInstances = setInstance(args.instance)

    if args.ping:
        for instance in artifactoryUrls:
            artifactoryInstance = connect(instance)

            if artifactoryInstance.getStatus().decode() == "OK":
                print("Artifactory in " + artifactoryLocation(instance) + " is up and running.")
            else:
                print("Houston, we have a problem.")
                sys.exit(13)

        sys.exit(0)

    if args.get_repositories:
        if args.rclass is None or args.type is None:
            print("--get-repositorie requires --rclass and --type")
            sys.exit(20)

        if args.rclass in repositoryClasses and args.type in repositoryTypes:
            for instance in artifactoryInstances:
                artifactoryInstance = connect(instance)
                repositories = artifactoryInstance.getRepositories(params = { 'type': args.rclass, 'packageType': args.type })

                print(repositories, end="\n\n")
        else:
            print("Wrong repository class or type. Please behave.")
            sys.exit(10)

        sys.exit(0)

    if args.create_repository:
        if args.name is None or args.rclass is None or args.type is None:
            print("--create-repository requires --name --rclass and --type")
            sys.exit(20)

        if args.rclass == "local":
            for instance in artifactoryInstances:
                artifactoryInstance = connect(instance)

                print("Creating repository in " + artifactoryLocation(instance) + " instance...")
                newRepository = artifactoryInstance.createRepository(args.name, data={
                    "key": args.name,
                    "rclass": args.rclass,
                    "packageType": args.type
                })

                print(newRepository, end="\n\n")
        else:
            print("Wrong repository class. Please behave.")
            sys.exit(10)

        sys.exit(0)

    if args.delete_repository:
        if args.name is None:
            print("--delete-repository requires --name")
            sys.exit(20)
        else:
            for instance in artifactoryInstances:
                artifactoryInstance = connect(instance)

                print("Deleting " + args.name + " repository in " + artifactoryLocation(instance) + "...")
                deleteRepository = artifactoryInstance.deleteRepository(args.name)
                print(deleteRepository)

            sys.exit(0)
