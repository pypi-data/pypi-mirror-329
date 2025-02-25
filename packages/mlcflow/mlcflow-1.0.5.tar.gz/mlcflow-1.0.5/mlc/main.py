import argparse
import subprocess
import re
import os
import importlib.util
import platform
import json
import yaml
import sys
import logging
from types import SimpleNamespace
import mlc.utils as utils
from pathlib import Path
from colorama import Fore, Style, init
import shutil

# Initialize colorama for Windows support
init(autoreset=True)
class ColoredFormatter(logging.Formatter):
    """Custom formatter class to add colors to log levels"""
    COLORS = {
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED
    }

    def format(self, record):
        # Add color to the levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

logger = logging.getLogger(__name__)

# Set up logging configuration
def setup_logging(log_path = os.getcwd(),log_file = 'mlc-log.txt'):
    
    if not logger.hasHandlers():
        logFormatter = ColoredFormatter('[%(asctime)s %(filename)s:%(lineno)d %(levelname)s] - %(message)s')
        logger.setLevel(logging.INFO)
   

        # File hander for logging in file in the specified path
        file_handler = logging.FileHandler("{0}/{1}".format(log_path, log_file))
        file_handler.setFormatter(logging.Formatter('[%(asctime)s %(filename)s:%(lineno)d %(levelname)s] - %(message)s'))
        logger.addHandler(file_handler)
    
        # Console handler for logging on console
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)
        logger.propagate = False


# Base class for CLI actions
class Action:
    repos_path = None
    cfg = None
    action_type = None
    logger = None
    local_repo = None
    current_repo_path = None
    #mlc = None
    repos = [] #list of Repo objects

    # Main access function to simulate a Python interface for CLI
    def access(self, options):
        """
        Access function to simulate CLI actions in Python.

        Args:
        options (dict): Dictionary containing action and relevant parameters.
        """
        #logger.info(f"options in access = {options}") 
        
        action_name = options.get('action')
        if not action_name:
            return {'return': 1, 'error': "'action' key is required in options"}
        #logger.info(f"options = {options}")

        action_target = options.get('target')
        if not action_target:
            action_target = options.get('automation', 'script')  # Default to script if not provided
        action_target_split = action_target.split(",")
        action_target = action_target_split[0]

        action = get_action(action_target, self)

        if action and hasattr(action, action_name):
            # Find the method and call it with the options
            method = getattr(action, action_name)
            result = method(options)
            #logger.info(f"result ={result}")
            return result
        else:
            return {'return': 1, 'error': f"'{action_name}' action is not supported for {action_target}."}
        return {'return': 0}

    def find_target_folder(self, target):
        # Traverse through each repo to find the first 'target' folder inside an 'automation' folder
        for repo in self.repos:
            repo_path = repo.path
            if os.path.isdir(repo_path):
                automation_folder = os.path.join(repo_path, 'automation')
                
                if os.path.isdir(automation_folder):
                    # Check if there's a 'script' folder inside the 'automation' folder
                    target_folder = os.path.join(automation_folder, target)
                    if os.path.isdir(target_folder):
                        return target_folder
        return None

    def load_repos_and_meta(self):
        repos_list = []
        repos_file_path = os.path.join(self.repos_path, 'repos.json')

        # Read the JSON file line by line
        try:
            # Load and parse the JSON file containing the list of repository paths
            with open(repos_file_path, 'r') as file:
                repo_paths = json.load(file)  # Load the JSON file into a list
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return []
        except FileNotFoundError:
            logger.error(f"Error: File {repos_file_path} not found.")
            return []
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return []
        
        def is_curdir_inside_path(base_path):
            # Convert to absolute paths
            base_path = Path(base_path).resolve()
            curdir = Path.cwd().resolve()

            # Check if curdir is inside base_path
            return base_path in curdir.parents or curdir == base_path

        # Iterate through the list of repository paths
        for repo_path in repo_paths:
            if not os.path.exists(repo_path):
                logger.warning(f"""Warning: {repo_path} not found. Considering it as a corrupt entry and deleting automatically...""")
                logger.warning(f"Deleting the {meta_yaml_path} entry from repos.json")
                res = self.access(
                    {
                        "automation": "repo",
                        "action": "rm",
                        "repo": f"{os.path.basename(repo_path)}"    
                    }
                )
                if res["return"] > 0:
                    return res
                continue

            if is_curdir_inside_path(repo_path):
                self.current_repo_path = repo_path
            repo_path = repo_path.strip()  # Remove any extra whitespace or newlines

           # Skip empty lines
            if not repo_path:
                continue

            meta_yaml_path = os.path.join(repo_path, "meta.yaml")

            # Check if meta.yaml exists
            if not os.path.isfile(meta_yaml_path):
                logger.warning(f"{meta_yaml_path} not found. Could be due to accidental deletion of meta.yaml. Try to stash the changes or reclone by doing `rm repo` and `pull repo`. Skipping...")
                continue

            # Load the YAML file
            try:
                with open(meta_yaml_path, 'r') as yaml_file:
                    meta = yaml.safe_load(yaml_file)
            except yaml.YAMLError as e:
                logger.error(f"Error loading YAML in {meta_yaml_path}: {e}")
                continue

            if meta['alias'] == "local":
                self.local_repo = f"""{meta['alias']},{meta['uid']}"""
            # Create a Repo object and add it to the list
            repos_list.append(Repo(path=repo_path, meta=meta))
        return repos_list

    def load_repos(self):
        # todo: what if the repo is already found in the repos folder but not registered and we pull the same repo
        # Get the path to the repos.json file in $HOME/MLC
        repos_file_path = os.path.join(self.repos_path, 'repos.json')

        # Check if the file exists
        if not os.path.exists(repos_file_path):
            logger.error(f"Error: File not found at {repos_file_path}")
            return None

        # Load and parse the JSON file
        try:
            with open(repos_file_path, 'r') as file:
                repos = json.load(file)
                return repos
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None
    

    def __init__(self):        
        setup_logging(log_path=os.getcwd(),log_file='mlc-log.txt')
        self.logger = logger

        temp_repo = os.environ.get('MLC_REPOS','').strip()
        if temp_repo == '':
            self.repos_path = os.path.join(os.path.expanduser("~"), "MLC", "repos")
        else:
            self.repos_path = temp_repo

        mlc_local_repo_path = os.path.join(self.repos_path, 'local')
        
        mlc_local_repo_path_expanded = Path(mlc_local_repo_path).expanduser().resolve()

        if not os.path.exists(mlc_local_repo_path):
            os.makedirs(mlc_local_repo_path, exist_ok=True)
        
        if not os.path.isfile(os.path.join(mlc_local_repo_path, "meta.yaml")):
            local_repo_meta = {"alias": "local", "name": "MLC local repository", "uid": utils.get_new_uid()['uid']}
            with open(os.path.join(mlc_local_repo_path, "meta.yaml"), "w") as json_file:
                json.dump(local_repo_meta, json_file, indent=4)
        
        # TODO: what if user changes the mlc local repo path in between
        repo_json_path = os.path.join(self.repos_path, "repos.json")
        if not os.path.exists(repo_json_path):
            with open(repo_json_path, 'w') as f:
                json.dump([str(mlc_local_repo_path_expanded)], f, indent=2)
                logger.info(f"Created repos.json in {os.path.dirname(self.repos_path)} and initialised with local cache folder path: {mlc_local_repo_path}")

        self.local_cache_path = os.path.join(mlc_local_repo_path, "cache")
        if not os.path.exists(self.local_cache_path):
            os.makedirs(self.local_cache_path, exist_ok=True)

        self.repos = self.load_repos_and_meta()
        #logger.info(f"In Action class: {self.repos_path}")
        self.index = Index(self.repos_path, self.repos)


        #self.repos = {
        #'lst': repo_paths
        #}

    def add(self, i):
        """
        Adds a new item to the repository.

        Args:
            i (dict): Input dictionary with the following keys:
                - item_repo (tuple): Repository alias and UID (default: local repo).
                - item (str): Item alias and optional UID in "alias,uid" format.
                - tags (str): Comma-separated tags.
                - new_tags (str): Additional comma-separated tags to add.
                - yaml (bool): Whether to save metadata in YAML format. Defaults to JSON.

        Returns:
            dict: Result of the operation with 'return' code and error/message if applicable.
        """
        # Determine repository
        item_repo = i.get("item_repo")
        if not item_repo:
            item_repo = self.local_repo
            

        # Parse item details
        item = i.get("item")

        item_name, item_id = (None, None)
        if item:
            item_parts = item.split(",")
            item_name = item_parts[0]
            if len(item_parts) > 1:
                item_id = item_parts[1]

        # Generate a new UID if not provided
        if not item_id:
            res = utils.get_new_uid()
            if res['return'] > 0:
                return res
            item_id = res['uid']

        # Locate repository
        res = self.access(
            {
                "automation": "repo",
                "action": "find",
                "item": f"{item_repo}",
            }
        )
        if res["return"] > 0:
            return res

        if len(res["list"]) == 0:
            return {'return': 1, 'error': f"""The given repo {item_repo} is not registered in MLC"""}

        # Determine paths and metadata format
        repo = res["list"][0]
        repo_path = repo.path
        
        target_name = i.get('target_name', self.action_type)
        target_path = os.path.join(repo_path, target_name)
        if target_name == "cache":
            folder_name = f"""{i["script_alias"]}_{item_name or item_id[:8]}""" if i.get("script_alias") else item_name or item_id
        else:
            folder_name = item_name or item_id

        item_path = os.path.join(target_path, folder_name)

        if os.path.exists(item_path):
            return {"return": 1, "error": f"""Item exists at {item_path}"""}

        # Create item directory if it does not exist
        os.makedirs(item_path)

        res = self.save_new_meta(i, item_id, item_name, target_name, item_path, repo)
        if res['return'] > 0:
            return res

        return {
            "return": 0,
            "message": f"Item successfully added at {item_path}",
            "path": item_path,
            "repo": repo
        }
    
    def rm(self, i):
        """
        Removes an item from the repository.

        Args:
            i (dict): Input dictionary with the following keys:
                - item_repo (tuple): Repository alias and UID (default: local repo).
                - item (str): Item alias and optional UID in "alias,uid" format.
                - tags (str): Comma-separated tags.
                - yaml (bool): Whether to save metadata in YAML format. Defaults to JSON.

        Returns:
            dict: Result of the operation with 'return' code and error/message if applicable.
        """
        inp = {}

        # Parse item details
        item = i.get("item",i.get('artifact', i.get('details')))
        item_name, item_id, item_tags = (None, None, None)
        if item:
            item_parts = item.split(",")
            item_name = item_parts[0]
            if len(item_parts) > 1:
                item_id = item_parts[1]
        elif i.get('tags'):
            item_tags = i['tags']
        else:
            if i.get('target_name', self.action_type) != "cache":
                return {'return': 1, 'error': 'Item not given for rm action'}
            else:
                inp['fetch_all'] = True

        # Check force remove is set to True
        # Setting force remove to true would lead to removal of assets without user prompt
        force_remove = True if i.get('f') else False

        if item_name:
            inp['alias'] = item_name
            inp['folder_name'] = item_name #we dont know if the user gave the alias or the folder name, we first check for alias and then the folder name
            if self.is_uid(item_name):
                inp['uid'] = item_name
        elif item_id:
            inp['uid'] = item_id
        if item_tags:
            inp['tags'] = item_tags

        target_name = i.get('target_name', self.action_type)
        inp['target_name'] = target_name
        res = self.search(inp)
        if res['return'] > 0:
            return res

        if len(res['list']) == 0:
            return {'return': 16, 'error': f'No {target_name} found for {inp}'}
        elif len(res['list']) > 1:
            logger.info(f"More than 1 {target_name} found for {inp}:")
            if not i.get('all'):
                for idx, item in enumerate(res["list"]):
                    logger.info(f"{idx}. Path: {item.path}, Meta: {item.meta}")

                if not force_remove:
                    user_choice = input("Would you like to proceed with all items? (yes/no): ").strip().lower()
                    if user_choice in ['yes', 'y']:
                        force_remove = True
                    
        results = res['list']
        
        for result in results:
            item_path = result.path
            item_meta = result.meta
        
        
            if os.path.exists(item_path):
                if force_remove == True:
                    shutil.rmtree(item_path)
                else:
                    user_choice = input(f"Confirm to delete {target_name} item: {item_path}? (yes/no): ").strip().lower()
                    if user_choice not in ['yes', 'y']:
                        continue
                    else:
                        shutil.rmtree(item_path)

                logger.info(f"{target_name} item: {item_path} has been successfully removed")

            self.index.rm(item_meta, target_name, item_path)
        
        return {
            "return": 0,
            "message": f"Item {item_path} successfully removed",
        }

    def save_new_meta(self, i, item_id, item_name, target_name, item_path, repo):
        # Prepare metadata
        item_meta = i.get('meta', {})
        item_meta.update({
            "alias": item_name,
            "uid": item_id,
        })

        # Process tags
        tags = i.get("tags", "").split(",") if i.get("tags") else item_meta.get("tags", [])
        new_tags = i.get("new_tags", "").split(",") if i.get("new_tags") else []

        item_meta["tags"] = list(set(tags + new_tags))  # Ensure unique tags

        # Save metadata
        meta_format = "yaml" if i.get("yaml") else "json"
        item_meta_path = os.path.join(item_path, f"meta.{meta_format}")

        if meta_format == "yaml":
            save_result = utils.save_yaml(item_meta_path, meta=item_meta)
        else:
            save_result = utils.save_json(item_meta_path, meta=item_meta)

        if save_result["return"] > 0:
            return save_result
    
        self.index.add(item_meta, target_name, item_path, repo)
        return {'return': 0}

    def update(self, i):
        """
        Update the tags of found items based on the input.

        Args:
            i (dict): Input dictionary with:
                - tags (str): Comma-separated tags to search for.
                - search_tags (str): Tags to add/update in the found items' meta.

        Returns:
            dict: Return code and message.
        """
        # Step 1: Search for items based on input tags
        target_name = i.get('target_name',"cache")
        i['target_name'] = target_name
        ii = i.copy()

        if i.get('search_tags'):
            ii['tags'] = ",".join(i['search_tags'])
        search_result = self.search(ii)
        if search_result['return'] > 0:
            return search_result

        found_items = search_result['list']
        if not found_items:
            res = self.add(i)
            if res['return'] > 0 :
                return res
            found_items.append(Item(res['path'], res['repo']))
            #return {'return': 0, 'message': 'No items found for the given tags.'}

        # Step 2: Prepare to update tags
        search_tags = i.get("search_tags", [])

        new_tags = set(search_tags)
        if len(found_items) > 1:
            # Step 3: Ask user for confirmation if multiple items are found
            user_input = input(f"{len(found_items)} items found. Do you want to update all? (yes/no): ").strip().lower()
            if user_input not in ['yes', 'y']:
                return {'return': 0, 'message': 'Update operation canceled by the user.'}

        new_meta = i.get('meta')
        if new_meta.get('tags'):
            new_meta['tags'] = i.get('tags').split(",")

        # Step 4: Update tags in each found item
        for item in found_items:
            meta = {}
            # Load the current meta of the item
            item_meta_path = os.path.join(item.path, "meta.json")
            if os.path.exists(item_meta_path):
                res = utils.load_json(item_meta_path)
                if res['return']> 0:
                    return res
                meta = res['meta']
            if i.get('replace_lists') and i.get("tags"):
                meta["tags"] = i["tags"].split(",")
            else:
                current_tags = set(meta.get("tags", []))
                updated_tags = current_tags.union(new_tags)
                meta["tags"] = list(updated_tags)
            utils.merge_dicts({"dict1": meta, "dict2": new_meta, "append_lists": True, "append_unique":True})
        
            # Save the updated meta back to the item
            item.meta = meta
            save_result = utils.save_json(item_meta_path, meta=meta)
            self.index.update(meta, target_name, item.path, item.repo)

        return {'return': 0, 'message': f"Tags updated successfully for {len(found_items)} item(s).", 'list': found_items }

    def is_uid(self, name):
        """
        Checks if the given name is a 16-digit hexadecimal UID.

        Args:
            name (str): The string to check.

        Returns:
            bool: True if the name is a 16-digit hexadecimal UID, False otherwise.
        """
        # Define a regex pattern for a 16-digit hexadecimal UID
        hex_uid_pattern = r"^[0-9a-fA-F]{16}$"

        # Check if the name matches the pattern
        return bool(re.fullmatch(hex_uid_pattern, name))


    def cp(self, run_args):
        action_target = run_args['target']
        if action_target != "script":
            return {"return": 1, "error": f"The {action_target} target is not currently supported for mv/cp actions"}
        inp = {}
        src_item = run_args.get('src')
        src_tags = None
        if src_item:
            src_split = src_item.split(":")
            if len(src_split) > 1:
                src_repo = src_split[0].strip()
                src_item = src_split[1].strip()
            else:
                src_item = src_split[0].strip()
            inp['alias'] = src_item
            inp['folder_name'] = src_item #we dont know if the user gave the alias or the folder name, we first check for alias and then the folder name
        
            if self.is_uid(src_item):
                inp['uid'] = src_item
            src_id = src_item
        else:
            #src_tags must be there
            if not run_args.get("src_tags"):
                return {'return': 1, 'error': 'Either "src" or "src_tags" must be provided as an input for cp method'}
            src_tags = run_args['src_tags']
            inp['tags'] = src_tags
            src_id = src_tags

        inp['target_name'] = action_target

        res = self.search(inp)

        choice = 0
        if len(res['list']) == 0:
            return {'return': 1, 'error': f'No {action_target} found for {src_id}'}
        elif len(res['list']) > 1 and not run_args.get("quiet"):
            print(f"More than one {action_target} found for {src_id}:")

            # Display available options
            for idx, item in enumerate(res['list'], start=1):
                print(f"{idx}. {item.path}")

            # Ask user to choose an item
            while True:
                choice = input("Select the correct one (enter number, default=1): ").strip()
                if choice == "":
                    choice = 1
                try:
                    choice = int(choice) - 1
                    if 0 <= choice < len(res['list']):
                        break
                    else:
                        print("Invalid selection. Please enter a number from the list.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        result = res['list'][choice]
        src_item_path = result.path
        src_item_meta = result.meta

        target_item = run_args['dest']
        target_split = target_item.split(":")

        if len(target_split) > 1:
            target_repo = target_split[0].strip()
            if target_repo == ".":
                if not self.current_repo_path:
                    return {'return': 1, 'error': f"""Current directory is not inside a registered MLC repo and so using ".:" is not valid"""}
                target_repo = self.current_repo_path
            else:
                if not any(os.path.basename(repodata.path) == target_repo for repodata in self.repos):
                    return {'return': 1, 'error': f"""The target repo {target_repo} is not registered in MLC. Either register in MLC by cloning from Git through command `mlc pull repo` or create repo using `mlc add repo` command and try to rerun the command again"""}
            target_repo_path = os.path.join(self.repos_path, target_repo)
            target_repo = Repo(target_repo_path)
            target_item_name = target_split[1].strip()
        else:
            target_repo = result.repo
            target_repo_path = result.repo.path
            target_item_name = target_split[0].strip()


        target_item_path = os.path.join(target_repo_path, action_target, target_item_name)
        res = self.copy_item(src_item_path, target_item_path)
        if res['return'] > 0:
            return res

        ii = {}
        ii['meta'] = result.meta.copy()
        if action_target == "script":
            ii['yaml'] = True

        tags = run_args.get('tags')
        item_id = run_args.get('item_id')

        if tags:
            ii['tags'] = tags

        # Generate a new UID if not provided
        if not item_id:
            res = utils.get_new_uid()
            if res['return'] > 0:
                return res
            item_id = res['uid']

        res = self.save_new_meta(ii, item_id, target_item_name, action_target, target_item_path, target_repo)

        dest_item = Item(target_item_path, target_repo)
        
        if res['return'] > 0:
            return res
        logger.info(f"{action_target} {src_item_path} copied to {target_item_path}")

        return {'return': 0, 'src': result, 'dest': dest_item}

    def copy_item(self, source_path, destination_path):
        try:
            # Copy the source folder to the destination
            shutil.copytree(source_path, destination_path)
            logger.info(f"Folder successfully copied from {source_path} to {destination_path}")
        except FileExistsError:
            return {'return': 1, 'error': f"Destination folder {destination_path} already exists."}
        except FileNotFoundError:
            return {'return': 1, 'error': f"Source folder {source_path} not found"}
        except Exception as e:
            return {'return': 1, 'error': f"An error occurred {e}"}

        return {'return': 0}

    def mv(self, run_args):
        target_name = run_args['target']
        if target_name != "script":
            return {"return": 1, "error": f"The {target_name} target is not currently supported for mv/cp actions"}
        res = self.cp(run_args)
        if res['return'] > 0:
            return res
        src = res['src']
        dest = res['dest']
        ii = {}
        ii['item'] = src.meta['uid']
        ii['f'] = True  # To remove the source without asking for user permission
        res = self.rm(ii)
        if res['return'] > 0:
            return res
        
        #Put the src uid to the destination path
        dest.meta['uid'] = src.meta['uid']
        dest._save_meta()
        self.index.update(dest.meta, target_name, dest.path, dest.repo)
        logger.info(f"""Item with uid {dest.meta['uid']} successfully moved from {src.path} to {dest.path}""")

        return {'return': 0, 'src': src, 'dest': dest}

    def search(self, i):
        indices = self.index.indices
        target = i.get('target_name', self.action_type)
        target_index = indices.get(target)
        result = []
        uid = i.get("uid")
        alias = i.get("alias")
        item_repo = i.get('item_repo')
        fetch_all = True if i.get('fetch_all') else False

        # For targets like cache, sometimes user would need to clear the entire cache folder present in the system
        # this helps to fetch entire data pertaining to particular target
        if fetch_all:
            for res in target_index:
                result.append(Item(res['path'], res['repo']))
            return {'return': 0, 'list': result}

        if not uid and not alias and i.get('details'):
            details = i['details']
            details_split = details.split(",")
            if len(details_split) > 1:
                alias = details_split[0]
                uid = details_split[1]
            else:
                if self.is_uid(details_split[0]):
                    uid = details_split[0]
                else:
                    alias = details_split[0]

        if alias and ":" in alias:
            alias_split = alias.split(":")
            alias = alias_split[1]
            item_repo = alias_split[0]
        folder_name = i.get("folder_name")
        found = False

        if item_repo:
            res = self.access(
                {
                    "action": "find",
                    "target": "repo",
                    "repo": f"{item_repo}"    
                }
            )
            if res["return"] > 0:
                return res
            if len(res['list']) == 0:
                return {'return': 1, 'error': f"""No repo found for {item_repo}"""}
            item_repo = res['list'][0]

        if target_index:
            if uid or alias:
                for res in target_index:
                    if (res["uid"] == uid or (alias and res["alias"] == alias)) and (not item_repo or item_repo == res['repo']):
                        it = Item(res['path'], res['repo'])
                        result.append(it)
                        found = True
                if not found and folder_name:
                    for res in target_index:
                        if os.path.basename(res["path"]) == folder_name:
                            it = Item(res['path'], res['repo'])
                            #result.append(it)
            else:
                tags = i.get("tags")
                if tags:
                    tags_split = tags.split(",")
                else:
                    return {"return":1, "error": f"Tags are not specifeid for completing the specific action"}
                if target == "script":
                    non_variation_tags = [t for t in tags_split if not t.startswith("_")]
                    tags_to_match = non_variation_tags
                elif target =="cache":
                    tags_to_match = tags_split
                else:
                    return {'return': 1, 'error': f"""Target {target} not handled in mlc yet"""}
                n_tags_ = [p for p in tags_to_match if p.startswith("-")]
                n_tags = [p[1:] for p in n_tags_]
                p_tags = list(set(tags_to_match) - set(n_tags_))
                for res in target_index:
                    c_tags = res["tags"]
                    if set(p_tags).issubset(set(c_tags)) and set(n_tags).isdisjoint(set(c_tags)):
                        it = Item(res['path'], res['repo'])
                        result.append(it)
        return {'return': 0, 'list': result}

    find = search


class Index:
    def __init__(self, repos_path, repos):
        """
        Initialize the Index class.
        
        Args:
            repos_path (str): Path to the base folder containing repositories.
        """
        self.repos_path = repos_path
        self.repos = repos
        #logger.info(repos)

        logger.debug(f"Repos path for Index: {self.repos_path}")
        self.index_files = {
            "script": os.path.join(repos_path, "index_script.json"),
            "cache": os.path.join(repos_path, "index_cache.json"),
            "experiment": os.path.join(repos_path, "index_experiment.json")
        }
        self.indices = {key: [] for key in self.index_files.keys()}
        self.build_index()

    def add(self, meta, folder_type, path, repo):
        unique_id = meta['uid']
        alias = meta['alias']
        tags = meta['tags']
        self.indices[folder_type].append({
                    "uid": unique_id,
                    "tags": tags,
                    "alias": alias,
                    "path": path,
                    "repo": repo
                })

    def get_index(self, folder_type, uid):
        for index in range(len(self.indices[folder_type])):
            if self.indices[folder_type][index]["uid"] == uid:
                return index
        return -1

    def update(self, meta, folder_type, path, repo):
        uid = meta['uid']
        alias = meta['alias']
        tags = meta['tags']
        index = self.get_index(folder_type, uid)
        if index == -1: #add it
            self.add(meta, folder_type, path, repo)
            logger.debug(f"Index update failed, new index created for {uid}")
        else:
            self.indices[folder_type][index] = {
                    "uid": uid,
                    "tags": tags,
                    "alias": alias,
                    "path": path,
                    "repo": repo
                }

    def rm(self, meta, folder_type, path):
        uid = meta['uid']
        index = self.get_index(folder_type, uid)
        if index == -1: 
            logger.warning(f"Index is not having the {folder_type} item {path}")
        else:
            del(self.indices[folder_type][index])

    def build_index(self):
        """
        Build shared indices for script, cache, and experiment folders across all repositories.
        
        Returns:
            None
        """

        #for repo in os.listdir(self.repos_path):
        for repo in self.repos:
            repo_path = repo.path#os.path.join(self.repos_path, repo)
            if not os.path.isdir(repo_path):
                continue

            # Filter for relevant directories in the repo
            for folder_type in ["script", "cache", "experiment"]:
                folder_path = os.path.join(repo_path, folder_type)
                if not os.path.isdir(folder_path):
                    continue

                # Process each automation directory
                for automation_dir in os.listdir(folder_path):
                    automation_path = os.path.join(folder_path, automation_dir)
                    if not os.path.isdir(automation_path):
                        continue

                    # Check for configuration files (meta.yaml or meta.json)
                    for config_file in ["meta.yaml", "meta.json"]:
                        config_path = os.path.join(automation_path, config_file)
                        if os.path.isfile(config_path):
                            self._process_config_file(config_path, folder_type, automation_path, repo)
                            break  # Only process one config file per automation_dir
        self._save_indices()

    def _process_config_file(self, config_file, folder_type, folder_path, repo):
        """
        Process a single configuration file (meta.json or meta.yaml) and add its data to the corresponding index.

        Args:
            config_file (str): Path to the configuration file.
            folder_type (str): Type of folder (script, cache, or experiment).
            folder_path (str): Path to the folder containing the configuration file.

        Returns:
            None
        """
        try:
            # Determine the file type based on the extension
            if config_file.endswith(".yaml") or config_file.endswith(".yml"):
                with open(config_file, "r") as f:
                    data = yaml.safe_load(f)
            elif config_file.endswith(".json"):
                with open(config_file, "r") as f:
                    data = json.load(f)
            else:
                logger.info(f"Skipping {config_file}: Unsupported file format.")
                return

            # Extract necessary fields
            unique_id = data.get("uid")
            tags = data.get("tags", [])
            alias = data.get("alias", None)

            # Validate and add to indices
            if unique_id:
                self.indices[folder_type].append({
                    "uid": unique_id,
                    "tags": tags,
                    "alias": alias,
                    "path": folder_path,
                    "repo": repo
                })
            else:
                logger.info(f"Skipping {config_file}: Missing 'uid' field.")
        except Exception as e:
            logger.error(f"Error processing {config_file}: {e}")


    def _save_indices(self):
        """
        Save the indices to JSON files.
        
        Returns:
            None
        """
        #logger.info(self.indices)
        for folder_type, index_data in self.indices.items():
            output_file = self.index_files[folder_type]
            try:
                with open(output_file, "w") as f:
                    json.dump(index_data, f, indent=4, cls=CustomJSONEncoder)
                logger.debug(f"Shared index for {folder_type} saved to {output_file}.")
            except Exception as e:
                logger.error(f"Error saving shared index for {folder_type}: {e}")

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Repo):
            # Customize how to serialize the Repo object
            return {
                "path": obj.path,
                "meta": obj.meta,
            }
        # For other unknown types, use the default behavior
        return super().default(obj)

class Item:
    def __init__(self, path, repo):
        self.meta = None
        self.path = path
        self.repo = repo
        self._load_meta()


    def _load_meta(self):
        yaml_file = os.path.join(self.path, "meta.yaml")
        json_file = os.path.join(self.path, "meta.json")

        if os.path.exists(yaml_file):
            self.meta = utils.read_yaml(yaml_file)
        elif os.path.exists(json_file):
            self.meta = utils.read_json(json_file)
        else:
            logger.info(f"No meta file found in {self.path} for {self.meta}")

    def _save_meta(self):
        yaml_file = os.path.join(self.path, "meta.yaml")
        json_file = os.path.join(self.path, "meta.json")

        if os.path.exists(yaml_file):
            utils.save_yaml(yaml_file, self.meta)
        elif os.path.exists(json_file):
            utils.save_json(json_file, self.meta)


class Repo:
    def __init__(self, path, meta=None):
        self.path = path
        if meta:
            self.meta = meta
        else:
            self._load_meta()
        
    
    def _load_meta(self):
        yaml_file = os.path.join(self.path, "meta.yaml")

        json_file = os.path.join(self.path, "meta.json")

        if os.path.exists(yaml_file):
            self.repo_meta = utils.read_yaml(yaml_file)
        elif os.path.exists(json_file):
            self.repo_meta = utils.read_json(json_file)
        else:
            logger.info(f"No meta file found in {self.path}")

class Automation:
    action_object = None
    automation_type = None
    meta = None
    path = None

    def __init__(self, action, automation_type, automation_file):
        #logger.info(f"action = {action}")
        self.action_object = action
        self.automation_type = automation_type
        self.path = os.path.dirname(automation_file)
        self._load_meta()

    def _load_meta(self):
        yaml_file = os.path.join(self.path, "meta.yaml")
        json_file = os.path.join(self.path, "meta.json")

        if os.path.exists(yaml_file):
            self.meta = utils.read_yaml(yaml_file)
        elif os.path.exists(json_file):
            self.meta = utils.read_json(json_file)
        else:
            logger.info(f"No meta file found in {self.path}")

    def search(self, i):
        indices = self.action_object.index.indices
        target_index = indices.get(self.automation_type)
        result = []
        if target_index:
            tags= i.get("tags")
            tags_split = tags.split(",")
            n_tags = [p for p in tags_split if p.startswith("-")]
            p_tags = list(set(tags_split) - set(n_tags))
            for res in target_index:
                c_tags = res["tags"]
                if set(p_tags).issubset(set(c_tags)) and set(n_tags).isdisjoint(set(c_tags)):
                    it = Item(res['path'], res['repo'])
                    result.append(it)
        #logger.info(result)
        return {'return': 0, 'list': result}
        #indices
        

# Child classes for specific entities (Repo, Script, Cache)
# Extends Action class
class RepoAction(Action):

    def __init__(self, parent=None):
        if parent is None:
            parent = default_parent
        #super().__init__(parent)
        self.parent = parent
        self.__dict__.update(vars(parent))


    def add(self, run_args):
        if not run_args['repo']:
            logger.error("The repository to be added is not specified")
            return {"return": 1, "error": "The repository to be added is not specified"}

        i_repo_path = run_args['repo'] #can be a path, forder_name or URL
        repo_folder_name = os.path.basename(i_repo_path)

        repo_path = os.path.join(self.repos_path, repo_folder_name)

        if os.path.exists(repo_path):
            return {'return': 1, "error": f"""Repo {run_args['repo']} already exists at {repo_path}"""}
        for repo in self.repos:
            if repo.path == i_repo_path:
                return {'return': 1, "error": f"""Repo {run_args['repo']} already exists at {repo_path}"""}

        if not os.path.exists(i_repo_path):
            #check if its an URL
            if utils.is_valid_url(i_repo_path):
                if "github.com" in i_repo_path:
                    res = self.github_url_to_user_repo_format(i_repo_path)
                    if res['return'] > 0:
                        return res
                    repo_folder_name = res['value']
                    repo_path = os.path.join(self.repos_path, repo_folder_name)

            os.makedirs(repo_path)
        else:
            repo_path = os.path.abspath(i_repo_path)
        logger.info(f"""New repo path: {repo_path}""")

        #check if it has MLC meta
        meta_file = os.path.join(repo_path, "meta.yaml")
        if not os.path.exists(meta_file):
            meta = {}
            meta['uid'] = utils.get_new_uid()['uid']
            meta['alias'] = repo_folder_name
            meta['git'] = True
            utils.save_yaml(meta_file, meta)
        else:
            meta = utils.read_yaml(meta_file)
        self.register_repo(repo_path, meta)

        return {'return': 0}

    def conflicting_repo(self, repo_meta):
        for repo_object in self.repos:
            if repo_object.meta.get('uid', '') == '':
                return {"return": 1, "error": f"UID is not present in file 'meta.yaml' in the repo path {repo_object.path}"}
            if repo_meta["uid"] == repo_object.meta.get('uid', ''):
                if repo_meta['path'] == repo_object.path:
                    return {"return": 1, "error": f"Same repo is already registered"}
                else:
                    return {"return": 1, "error": f"Conflicting with repo in the path {repo_object.path}", "conflicting_path": repo_object.path}
        return {"return": 0}
    
    def register_repo(self, repo_path, repo_meta):
    
        if repo_meta.get('deps'):
            for dep in repo_meta['deps']:
                self.pull_repo(dep['url'], branch=dep.get('branch'), checkout=dep.get('checkout'))

        # Get the path to the repos.json file in $HOME/MLC
        repos_file_path = os.path.join(self.repos_path, 'repos.json')

        with open(repos_file_path, 'r') as f:
            repos_list = json.load(f)
        
        if repo_path not in repos_list:
            repos_list.append(repo_path)
            logger.info(f"Added new repo path: {repo_path}")

        with open(repos_file_path, 'w') as f:
            json.dump(repos_list, f, indent=2)
            logger.info(f"Updated repos.json at {repos_file_path}")
        return {'return': 0}

    def unregister_repo(self, repo_path):
        logger.info(f"Unregistering the repo in path {repo_path}")
        repos_file_path = os.path.join(self.repos_path, 'repos.json')

        with open(repos_file_path, 'r') as f:
            repos_list = json.load(f)
        
        if repo_path in repos_list:
            repos_list.remove(repo_path)
            with open(repos_file_path, 'w') as f:
                json.dump(repos_list, f, indent=2)  
            logger.info(f"Path: {repo_path} has been removed.")
        else:
            logger.info(f"Path: {repo_path} not found in {repos_file_path}. Nothing to be unregistered!")
        return {'return': 0}

    def find(self, run_args):
        try:
            # Get repos_list using the existing method
            repos_list = self.load_repos_and_meta()
            if(run_args.get('item', run_args.get('artifact'))):
                repo = run_args.get('item', run_args.get('artifact'))
            else:
                repo = run_args.get('repo', run_args.get('item', run_args.get('artifact')))

            # Check if repo is None or empty
            if not repo:
                return {"return": 1, "error": "Please enter a Repo Alias, Repo UID, or Repo URL in one of the following formats:\n"
                                         "- <repo_owner>@<repos_name>\n"
                                         "- <repo_url>\n"
                                         "- <repo_uid>\n"
                                         "- <repo_alias>\n"
                                         "- <repo_alias>,<repo_uid>"}

            # Handle the different repo input formats
            repo_name = None
            repo_uid = None

            # Check if the repo is in the format of a repo UID (alphanumeric string)
            if self.is_uid(repo):
                repo_uid = repo
            if "," in repo:
                repo_split = repo.split(",")
                repo_name = repo_split[0]
                if len(repo_split) > 1:
                    repo_uid = repo_split[1]
            elif "@" in repo:
                repo_name = repo
            elif "github.com" in repo:
                result = self.github_url_to_user_repo_format(repo)
                if result["return"] == 0:
                    repo_name = result["value"]
                else:
                    return result
            
            # Check if repo_name exists in repos.json
            matched_repo_path = None
            for repo_obj in repos_list:
                if repo_name and repo_name == os.path.basename(repo_obj.path) :
                    matched_repo_path = repo_obj
                    break

            # Search through self.repos for matching repos
            lst = []
            for i in self.repos:
                if repo_uid and i.meta['uid'] == repo_uid:
                    lst.append(i)
                elif repo_name == i.meta['alias']:
                    lst.append(i)
                elif self.is_uid(repo) and not any(i.meta['uid'] == repo_uid for i in self.repos):
                    return {"return": 1, "error": f"No repository with UID: '{repo_uid}' was found"}
                elif "," in repo and not matched_repo_path and not any(i.meta['uid'] == repo_uid for i in self.repos) and not any(i.meta['alias'] == repo_name for i in self.repos):
                    return {"return": 1, "error": f"No repository with alias: '{repo_name}' and UID: '{repo_uid}' was found"}
                elif not matched_repo_path and not any(i.meta['alias'] == repo_name for i in self.repos) and not any(i.meta['uid'] == repo_uid for i in self.repos ):
                    return {"return": 1, "error": f"No repository with alias: '{repo_name}' was found"}
                
            # Append the matched repo path
            if(len(lst)==0):
                lst.append(matched_repo_path)
            
            return {'return': 0, 'list': lst}
        except Exception as e:
            # Return error message if any exception occurs
            return {"return": 1, "error": str(e)}

    def github_url_to_user_repo_format(self, url):
        """
        Converts a GitHub repo URL to user@repo_name format.

        :param url: str, GitHub repository URL (e.g., https://github.com/user/repo_name.git)
        :return: str, formatted as user@repo_name
        """
        import re

        # Regex to match GitHub URLs
        pattern = r"(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/.]+)(?:\.git)?"

        match = re.match(pattern, url)
        if match:
            user, repo_name = match.groups()
            return {"return": 0, "value": f"{user}@{repo_name}"}
        else:
            return {"return": 0, "value": os.path.basename(url).replace(".git", "")}

    def pull_repo(self, repo_url, branch=None, checkout = None, tag = None, pat = None, ssh = None):
        
        # Determine the checkout path from environment or default
        repo_base_path = self.repos_path # either the value will be from 'MLC_REPOS'
        os.makedirs(repo_base_path, exist_ok=True)  # Ensure the directory exists

        # Handle user@repo format (convert to standard GitHub URL)
        if re.match(r'^[\w-]+@[\w-]+$', repo_url):
            user, repo = repo_url.split('@')
            repo_url = f"https://github.com/{user}/{repo}.git"

        # support pat and ssh
        if pat or ssh:
            tmp_param = {}
            url_type = "pat" if pat else "ssh"
            if pat:
                tmp_param["token"] = pat
            res = utils.modify_git_url(url_type, repo_url, tmp_param)
            if res["return"] > 0:
                return res
            else:
                print(res)
                repo_url = res["url"]
            

        # Extract the repo name from URL
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        res = self.github_url_to_user_repo_format(repo_url)
        if res["return"] > 0:
            return res
        else:
            repo_download_name = res["value"]
            repo_path = os.path.join(repo_base_path, repo_download_name)

        try:
            # If the directory doesn't exist, clone it
            if not os.path.exists(repo_path):
                logger.info(f"Cloning repository {repo_url} to {repo_path}...")
                
                # Build clone command without branch if not provided
                clone_command = ['git', 'clone', repo_url, repo_path]
                if branch:
                    clone_command = ['git', 'clone', '--branch', branch, repo_url, repo_path]
                
                subprocess.run(clone_command, check=True)

            else:
                logger.info(f"Repository {repo_name} already exists at {repo_path}. Checking for local changes...")
    
                # Check for local changes
                status_command = ['git', '-C', repo_path, 'status', '--porcelain', '--untracked-files=no']
                local_changes = subprocess.run(status_command, capture_output=True, text=True)

                if local_changes.stdout.strip():
                    logger.warning("There are local changes in the repository. Please commit or stash them before checking out.")
                    return {"return": 0, "warning": f"Local changes detected in the already existing repository: {repo_path}, skipping the pull"}
                else:
                    logger.info("No local changes detected. Fetching latest changes...")
                    subprocess.run(['git', '-C', repo_path, 'fetch'], check=True)
            
            if tag:
                checkout = "tags/"+tag

            # Checkout to a specific branch or commit if --checkout is provided
            if checkout or tag:
                logger.info(f"Checking out to {checkout} in {repo_path}...")
                subprocess.run(['git', '-C', repo_path, 'checkout', checkout], check=True)
            
            if not tag:
                subprocess.run(['git', '-C', repo_path, 'pull'], check=True)

            logger.info("Repository successfully pulled.")
            logger.info("Registering the repo in repos.json")

            # check the meta file to obtain uids
            meta_file_path = os.path.join(repo_path, 'meta.yaml')
            if not os.path.exists(meta_file_path):
                logger.warning(f"meta.yaml not found in {repo_path}. Repo pulled but not register in mlc repos. Skipping...")
                return {"return": 0}
            
            with open(meta_file_path, 'r') as meta_file:
                meta_data = yaml.safe_load(meta_file)
                meta_data["path"] = repo_path

            # Check UID conflicts
            is_conflict = self.conflicting_repo(meta_data)
            if is_conflict['return'] > 0:
                if "UID not present" in is_conflict['error']:
                    logger.warning(f"UID not found in meta.yaml at {repo_path}. Repo pulled but can not register in mlc repos. Skipping...")
                    return {"return": 0}
                elif "already registered" in is_conflict["error"]:
                    #logger.warning(is_conflict["error"])
                    logger.info("No changes made to repos.json.")
                    return {"return": 0}
                else:
                    logger.warning(f"The repo to be cloned has conflict with the repo already in the path: {is_conflict['conflicting_path']}")
                    self.unregister_repo(is_conflict['conflicting_path'])
                    self.register_repo(repo_path, meta_data)
                    logger.warning(f"{repo_path} is registered in repos.json and {is_conflict['conflicting_path']} is unregistered.")
                    return {"return": 0}
            else:         
                r = self.register_repo(repo_path, meta_data)
                if r['return'] > 0:
                    return r
                return {"return": 0}

        except subprocess.CalledProcessError as e:
            return {'return': 1, 'error': f"Git command failed: {e}"}
        except Exception as e:
            return {'return': 1, 'error': f"Error pulling repository: {str(e)}"}

    def pull(self, run_args):
        repo_url = run_args.get('repo', run_args.get('url', 'repo'))
        if not repo_url or repo_url == "repo":
            for repo_object in self.repos:
                repo_folder_name = os.path.basename(repo_object.path)
                if "@" in repo_folder_name:
                    res = self.pull_repo(repo_folder_name)
                    if res['return'] > 0:
                        return res
        else:
            branch = run_args.get('branch')
            checkout = run_args.get('checkout')
            tag = run_args.get('tag')

            pat = run_args.get('pat')
            ssh = run_args.get('ssh')

            if sum(bool(var) for var in [branch, checkout, tag]) > 1:
                    return {"return": 1, "error": "Only one among the three flags(branch, checkout and tag) could be specified"}
            
            res = self.pull_repo(repo_url, branch, checkout, tag, pat, ssh)
            if res['return'] > 0:
                return res

        return {'return': 0}

            
    def list(self, run_args):
        logger.info("Listing all repositories.")
        print("\nRepositories:")
        print("-------------")
        for repo_object in self.repos:
            print(f"- Alias: {repo_object.meta.get('alias', 'Unknown')}")
            print(f"  Path:  {repo_object.path}\n")
        print("-------------")
        logger.info("Repository listing ended")
        return {"return": 0}
    
    def rm(self, run_args):
        logger.info("rm command has been called for repo. This would delete the repo folder and unregister the repo from repos.json")
        
        if not run_args['repo']:
            logger.error("The repository to be removed is not specified")
            return {"return": 1, "error": "The repository to be removed is not specified"}
        
        force_remove = True if run_args.get('f') else False

        repo_folder_name = run_args['repo']

        repo_path = os.path.join(self.repos_path, repo_folder_name)

        if os.path.exists(repo_path):
            # Check for local changes
            status_command = ['git', '-C', repo_path, 'status', '--porcelain', '--untracked-files=no']
            local_changes = subprocess.run(status_command, capture_output=True, text=True)

            if local_changes.stdout:
                logger.warning("Local changes detected in repository. Changes are listed below:")
                print(local_changes.stdout)
                confirm_remove = True if force_remove or (input("Continue to remove repo?").lower()) in ["yes", "y"] else False
            else:
                logger.info("No local changes detected. Removing repo...")
                confirm_remove = True
            if confirm_remove:
                if force_remove:
                    logger.info("Force remove is set.")
                shutil.rmtree(repo_path)
                logger.info(f"Repo {run_args['repo']} residing in path {repo_path} has been successfully removed")
                logger.info("Checking whether the repo was registered in repos.json")
                self.unregister_repo(repo_path)
            else:
                logger.info("rm repo ooperation cancelled by user!")
        else:
            logger.warning(f"Repo {run_args['repo']} was not found in the repo folder. repos.json will be checked for any corrupted entry. If any, that will be removed.")
            self.unregister_repo(repo_path)

        return {"return": 0}
        

class ScriptAction(Action):
    parent = None
    def __init__(self, parent=None):
        if parent is None:
            parent = default_parent
        self.parent = parent
        self.__dict__.update(vars(parent))

    def search(self, i):
        if not i.get('target_name'):
            i['target_name'] = "script"
        res = self.parent.search(i)
        #print(res)
        return res

    find = search
        
    def rm(self, i):
        if not i.get('target_name'):
            i['target_name'] = "script"
        logger.debug(f"Removing script with input: {i}")
        return self.parent.rm(i)

    def show(self, run_args):
        self.action_type = "script"
        res = self.search(run_args)
        if res['return'] > 0:
            return res
        logger.info(f"Showing script with tags: {run_args.get('tags')}")
        script_meta_keys_to_show = ["uid", "alias", "tags", "new_env_keys", "new_state_keys", "cache"]
        for item in res['list']:
            print(f"""Location: {item.path}:
Main Script Meta:""")
            for key in script_meta_keys_to_show:
                if key in item.meta:
                    print(f"""    {key}: {item.meta[key]}""")
            if "input_mapping" in item.meta:
                print("    Input mapping:")
                utils.printd(item.meta["input_mapping"], begin_spaces=8)
            print("......................................................")
            print(f"""For full script meta, see meta file at {os.path.join(item.path, "meta.yaml")}""")
            print("")
            
        return {'return': 0}

    def add(self, i):
        """
        Adds a new script to the repository.

        Args:
            i (dict): Input dictionary with the following keys:
                - item_repo (tuple): Repository alias and UID (default: local repo).
                - item (str): Item alias and optional UID in "alias,uid" format.
                - tags (str): Comma-separated tags.
                - yaml (bool): Whether to save metadata in YAML format. Defaults to JSON.

        Returns:
            dict: Result of the operation with 'return' code and error/message if applicable.
        """
        # Determine repository
        if i.get('details'):
            item = i['details']
        else:
            item = i.get('item')
        if not item:
            return {'return': 1, 'error': f"""No script item given to add. Please use mlc add script <repo_name>:<script_name> --tags=<script_tags> format to add a script to a given repo"""}
        ii = {}
        ii['target'] = "script"
        ii['src_tags'] = i.get("template_tags", "template,generic")
        ii['dest'] = item
        ii['tags'] = i.get('tags', [])
        res =  self.cp(ii)

        return res

    def dynamic_import_module(self, script_path):
        # Validate the script_path
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script file not found: {script_path}")

        # Add the parent folder of the script to sys.path
        script_dir = os.path.dirname(script_path)
        automation_dir = os.path.dirname(script_dir)  # automation folder

        if automation_dir not in sys.path:
            sys.path.insert(0, automation_dir)

        # Dynamically load the module
        module_name = os.path.splitext(os.path.basename(script_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot create a module spec for: {script_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    def call_script_module_function(self, function_name, run_args):
        self.action_type = "script"
        repos_folder = self.repos_path

        # Import script submodule 
        script_path = self.find_target_folder("script")
        if not script_path:
            return {'return': 1, 'error': f"""Script automation not found. Have you done "mlc pull repo mlcommons@mlperf-automations --branch=dev"?"""}

        module_path = os.path.join(script_path, "module.py")
        module = self.dynamic_import_module(module_path)


        # Check if ScriptAutomation is defined in the module
        if hasattr(module, 'ScriptAutomation'):
            automation_instance = module.ScriptAutomation(self, module_path)
            if function_name == "run":
                result = automation_instance.run(run_args)  # Pass args to the run method
            elif function_name == "docker":
                result = automation_instance.docker(run_args)  # Pass args to the run method
            elif function_name == "test":
                result = automation_instance.test(run_args)  # Pass args to the run method
            else:
                return {'return': 1, 'error': f'Function {function_name} is not supported'}
            
            if result['return'] > 0:
                error = result.get('error', "")
                raise ScriptExecutionError(f"Script {function_name} execution failed. Error : {error}")
            return result
        else:
            logger.info("ScriptAutomation class not found in the script.")
            return {'return': 1, 'error': 'ScriptAutomation class not found in the script.'}

    def docker(self, run_args):
        return self.call_script_module_function("docker", run_args)

    def run(self, run_args):
        return self.call_script_module_function("run", run_args)

    def test(self, run_args):
        return self.call_script_module_function("test", run_args)


    def list(self, args):
        self.action_type = "script"
        run_args = {"fetch_all": True}  # to fetch the details of all the scripts present in repos registered  in mlc
        
        res = self.search(run_args)
        if res['return'] > 0:
            return res
        
        logger.info(f"Listing all the scripts and their paths present in repos which are registered in MLC")
        print("......................................................")
        for item in res['list']:
            print(f"alias: {item.meta['alias'] if item.meta.get('alias') else 'None'}")
            print(f"Location: {item.path}")
            print("......................................................")

        return {"return": 0}


class ScriptExecutionError(Exception):
    """Custom error for configuration issues."""
    pass

class CacheAction(Action):

    def __init__(self, parent=None):
        if parent is None:
            parent = default_parent
        #super().__init__(parent)
        self.parent = parent
        self.__dict__.update(vars(parent))
    
    def search(self, i):
        i['target_name'] = "cache"
        #logger.debug(f"Searching for cache with input: {i}")
        return self.parent.search(i)

    find = search

    def rm(self, i):
        i['target_name'] = "cache"
        #logger.debug(f"Removing cache with input: {i}")
        return self.parent.rm(i)

    def show(self, run_args):
        self.action_type = "cache"
        res = self.search(run_args)
        logger.info(f"Showing cache with tags: {run_args.get('tags')}")
        cached_meta_keys_to_show = ["uid", "tags", "dependent_cached_path", "associated_script_item"]
        cached_state_keys_to_show = ["new_env", "new_state", "version"]
        for item in res['list']:
            print(f"""Location: {item.path}:
Cache Meta:""")
            for key in cached_meta_keys_to_show:
                if key in item.meta:
                    print(f"""    {key}: {item.meta[key]}""")
            print("""Cached State:""")
            cached_state_meta_file = os.path.join(item.path, "mlc-cached-state.json")
            if not os.path.exists(cached_state_meta_file):
                continue
            try:
                # Load and parse the JSON file containing the cached state
                with open(cached_state_meta_file, 'r') as file:
                    meta = json.load(file)
                    for key in cached_state_keys_to_show:
                        if key in meta:
                            print(f"""    {key}:""", end="")
                            if meta[key] and isinstance(meta[key], dict):
                                print("")
                                utils.printd(meta[key], yaml=False, sort_keys=True, begin_spaces=8)
                            else:
                                print(f""" {meta[key]}""")
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}")
            print("......................................................")
            print("")
            
        return {'return': 0}

    def list(self, args):
        self.action_type = "cache"
        run_args = {"fetch_all": True}  # to fetch the details of all the caches generated
        
        res = self.search(run_args)
        if res['return'] > 0:
            return res
        
        logger.info(f"Listing all the caches and their paths")
        print("......................................................")
        for item in res['list']:
            print(f"tags: {item.meta['tags'] if item.meta.get('tags') else 'None'}")
            print(f"Location: {item.path}")
            print("......................................................")

        return {'return': 0}

class ExperimentAction(Action):
    def __init__(self, parent=None):
        if parent is None:
            parent = default_parent
        #super().__init__(parent)
        self.parent = parent
        self.__dict__.update(vars(parent))

    def show(self, args):
        logger.info(f"Showing experiment with identifier: {args.details}")
        return {'return': 0}

    def list(self, args):
        logger.info("Listing all experiments.")
        return {'return': 0}


class CfgAction(Action):
    def __init__(self, parent=None):
        if parent is None:
            parent = default_parent
        #super().__init__(parent)
        self.parent = parent
        self.__dict__.update(vars(parent))

    def load(self, args):
        """
        Load the configuration.
        
        Args:
            args (dict): Contains the configuration details such as file path, etc.
        """
        #logger.info("In cfg load")
        default_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
        config_file = args.get('config_file', default_config_path)
        logger.info(f"In cfg load, config file = {config_file}")
        if not config_file or not os.path.exists(config_file):
            logger.error(f"Error: Configuration file '{config_file}' not found.")
            return {'return': 1, 'error': f"Error: Configuration file '{config_file}' not found."}
        
        #logger.info(f"Loading configuration from {config_file}")
        
        # Example loading YAML configuration (can be modified based on your needs)
        try:
            with open(config_file, 'r') as file:
                config_data = yaml.safe_load(file)
                logger.info(f"Loaded configuration: {config_data}")
                # Store configuration in memory or perform other operations
                self.cfg = config_data
        except yaml.YAMLError as e:
            logger.error(f"Error loading YAML configuration: {e}")
        
        return {'return': 0, 'config': self.cfg}


actions = {
        'repo': RepoAction,
        'script': ScriptAction,
        'cache': CacheAction,
        'cfg': CfgAction,
        'experiment': ExperimentAction
    }

# Factory to get the appropriate action class
def get_action(target, parent):
    action_class = actions.get(target, None)
    return action_class(parent) if action_class else None


def access(i):
    action = i['action']
    target = i.get('target', i.get('automation'))
    action_class = get_action(target, default_parent)
    r = action_class.access(i)
    return r

def mlcr():
    first_arg_value = "run"
    second_arg_value = "script"

    # Insert the positional argument into sys.argv for the main function
    sys.argv.insert(1, first_arg_value)
    sys.argv.insert(2, second_arg_value)

    # Call the main function
    main()

default_parent = None

if default_parent is None:
    default_parent = Action()

def process_console_output(res, target, action, run_args):
    if action in ["find", "search"]:
        if "list" not in res:
            logger.error("'list' entry not found in find result")
            return  # Exit function if there's an error
        if len(res['list']) == 0:
            logger.warning(f"""No {target} entry found for the specified input: {run_args}!""")
        else:
            for item in res['list']:
                logger.info(f"""Item path: {item.path}""")

# Main CLI function
def main():
    parser = argparse.ArgumentParser(prog='mlc', description='A CLI tool for managing repos, scripts, and caches.')

    # Subparsers are added to main parser, allowing for different commands (subcommands) to be defined. 
    # The chosen subcommand will be stored in the "command" attribute of the parsed arguments.
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Script and Cache-specific subcommands
    for action in ['run', 'pull', 'test', 'add', 'show', 'list', 'find', 'search', 'rm', 'cp', 'mv']:
        action_parser = subparsers.add_parser(action, help=f'{action} a target.')
        action_parser.add_argument('target', choices=['repo', 'script', 'cache'], help='Target type (repo, script, cache).')
        # the argument given after target and before any extra options like --tags will be stored in "details"
        action_parser.add_argument('details', nargs='?', help='Details or identifier (optional for list).')
        action_parser.add_argument('extra', nargs=argparse.REMAINDER, help='Extra options (e.g.,  -v)')

    # Script and specific subcommands
    for action in ['docker', 'help']:
        action_parser = subparsers.add_parser(action, help=f'{action.capitalize()} a target.')
        action_parser.add_argument('target', choices=['script', 'run'], help='Target type (script).')
        # the argument given after target and before any extra options like --tags will be stored in "details"
        action_parser.add_argument('details', nargs='?', help='Details or identifier (optional for list).')
        action_parser.add_argument('extra', nargs=argparse.REMAINDER, help='Extra options (e.g.,  -v)')

    for action in ['load']:
        load_parser = subparsers.add_parser(action, help=f'{action.capitalize()} a target.')
        load_parser.add_argument('target', choices=['cfg'], help='Target type (cfg).')
    
    
    # Parse arguments
    args = parser.parse_args()

    #logger.info(f"Args = {args}")

    res = utils.convert_args_to_dictionary(args.extra)
    if res['return'] > 0:
        return res

    run_args = res['args_dict']
    if hasattr(args, 'repo') and args.repo:
        run_args['repo'] = args.repo
        
    if args.command in ['pull', 'rm', 'add', 'find']:
        if args.target == "repo":
            run_args['repo'] = args.details
  
    if args.command in ['docker']:
        if args.target == "run":
            run_args['target'] = 'script' #allowing run to be used for docker run instead of docker script
            args.target = "script"

    if hasattr(args, 'details') and args.details and "," in args.details and not run_args.get("tags") and args.target in ["script", "cache"]:
        run_args['tags'] = args.details

    if not run_args.get('details') and args.details:
        run_args['details'] = args.details

    if args.command in ["cp", "mv"]:
        run_args['target'] = args.target
        if hasattr(args, 'details') and args.details:
            run_args['src'] = args.details
        if hasattr(args, 'extra') and args.extra:
            run_args['dest'] = args.extra[0]

    # Get the action handler for other commands
    action = get_action(args.target, default_parent)
    # Dynamically call the method (e.g., run, list, show)
    if action and hasattr(action, args.command):
        method = getattr(action, args.command)
        res = method(run_args)
        if res['return'] > 0:
            logger.error(res.get('error', f"Error in {action}"))
            raise Exception(f"""An error occurred {res}""")
        process_console_output(res, args.target, args.command, run_args)
    else:
        logger.error(f"Error: '{args.command}' is not supported for {args.target}.")

if __name__ == '__main__':
    main()

