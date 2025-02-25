'''
This python program must be in the same directory as the zarf.yaml file to work properly.
'''
import yaml
import subprocess

# Path to your zarf.yaml file
zarf_yaml_path = 'zarf.yaml'

def main():
    create_zarf_config(zarf_yaml_path)
    inject_images(get_image_list())
    return

def create_zarf_config(yaml_file):
    '''
    This function extracts the variables from the zarf.yaml file and creates the zarf-config.toml 
    file to bypass the prompt input when running zarf dev find-images
    '''
    with open(yaml_file, 'r') as file:
        # Load the YAML data
        data = yaml.safe_load(file)
        extracted_var_list = []
        extracted_var_list.append("[package.deploy.set]\n")
        # Check if variables exist and print them
        if 'variables' in data:
            variables = data['variables']
            # loops through the available variables and formats them before appending them to extracted_var_list
            for var in variables:
                extracted_var_list.append(f"{var.get('name')} = '{var.get('default', '')}'\n")
    # Creates the zarf-config.toml and writes the extracted variables
    with open('zarf-config.toml', 'w') as file:
        file.writelines(extracted_var_list)
        
####################################################################################################################################
def get_image_list():
    '''
    Grabs the image list from the zarf dev find-images command, cleans the data, and then returns the list.
This command 
    '''
    # Initialize the image list
    image_list = []

    # Run the zarf dev find-images command
    find_images_command = ["zarf", "dev", "find-images"]
    images = subprocess.run(find_images_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    images = images.stdout.split('\n')
        # Loops through and cleans the data before adding it to the image_list
    for _ in images[5::]:
        if _ == "":
            continue
        _ = _.lstrip("- ").lstrip(" ").strip().strip(' ').replace('\n', " ")
        image_list.append(_)
            
    return image_list

####################################################################################################################################
def inject_images(image_list):
    '''
    Uses the yaml module to replace the image list in the zarf.yaml file with the most recent image list
    '''
    with open(zarf_yaml_path, 'r') as file:
        # Load the YAML data
        data = yaml.safe_load(file)
    
    if "components" in data:
        for component in data["components"]:
            if "images" in component:
                component["images"] = image_list
            else:
                component.update({"images": image_list})
        
            
    with open(zarf_yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
        
    return data

if __name__ == "__main__":
    
    main()
