from mc_server_tool.src.downloads import get_forge_link, get_neoforge_link, get_serverjar_link
from mc_server_tool.src.globals import PACKAGES


def test_server_links():
    for package in PACKAGES:
        print(f"Testing link for {package}!...")
        if package == "Mohist" or package == "Folia":
            version = "1.20.1"
        else:
            version = "1.21"

        if package == "Forge":
            url = get_forge_link(version)
        elif package == "Neoforge":
            url = get_neoforge_link(version)
        else:
            url = get_serverjar_link(version, package)

        if url is None:
            print(f"Failed to get jar file from Package: {package}")
        else:
            if package == "Mohist" or package == "Purpur":
                if not version in url:
                    print(f"Failed to get jar file from Package: {package}")
                else:
                    print("Success")
            else:
                if not ".jar" in url:
                    print(f"Failed to get jar file from Package: {package}")
                else:
                    print("Success")


if __name__ == "__main__":
    test_server_links()
