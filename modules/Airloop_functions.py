from modules.import_libs import *

def short_road_name(road_path):
    """
    Shortens the road name for path-related issues.

    Args:
        road_path (str): The path or name of the road.

    Returns:
        str: The shortened road name.
    """
    short_name = ''
    if os.path.isdir(road_path):
        road_name = road_path.split(os.sep)[3]
        new_name_list = road_name.split()
        for i in range(len(new_name_list)):
            short_name += new_name_list[i][0].upper()
        return short_name
    else:
        new_name_list = road_path.split()
        for i in range(len(new_name_list)):
            short_name += new_name_list[i][0].upper()
        return short_name   


def find_district_directory():
    """
    Finds the district directory within the current directory.

    Returns:
        str: The name of the district directory.
    """
    return [i for i in next(os.walk('Data'))[1]][0]

def find_road_directories(district):
    """
    Finds all road directories within a district.

    Args:
        district (str): The name of the district.

    Returns:
        list: A list of road directories.
    """
    return [i for i in (glob.glob(district + os.sep + 'roads' + os.sep + '*')) if os.path.isdir(i)]



def extract_lat_long_from_srt(srt_file_path):
    with open(srt_file_path, 'r') as file:
        srt_content = file.read()

    # Regular expression to match the latitude and longitude in the given format
    lat_long_pattern = re.compile(r'\[latitude: (?P<lat>-?\d+\.\d+)\] \[longitude: (?P<long>-?\d+\.\d+)\]')

    # Find all latitude and longitude matches
    lat_longs = lat_long_pattern.findall(srt_content)

    if not lat_longs:
        raise ValueError("No GPS coordinates found in the SRT file:",os.path.basename(srt_file_path))

    # Extract the first and last GPS coordinates
    start_lat, start_long = lat_longs[0]
    end_lat, end_long = lat_longs[-1]

    return (start_lat, start_long), (end_lat, end_long)



#PCI color_mapping ((((note: color codes are changed as comp. to summary file function))))
def get_pci_color(pci_value): 
    """
    Get the color associated with a PCI (Pavement Condition Index) value.
    This function takes a PCI value and returns the corresponding color based on predefined ranges.
    
    Returns:
    str: The color code in hexadecimal format.

    Note:
    - The function uses predefined PCI value ranges and their associated colors to determine the color.
    - If the provided PCI value is not within any of the defined ranges, it returns the default color '#000000'.
    """
    
    pci_value=int(pci_value)
    
    pci_color_mapping = {
        range(0, 11): '#bf9000',
        range(11, 26): '#89081d',
        range(26, 41): '#c00000',
        range(41, 56): '#ff0000',
        range(56, 71): '#ffff00',
        range(71, 86): '#92d050',
        range(86, 101): '#009051'
    }
    pci_color = '#000000'  # Default color if none of the ranges match
    for pci_range, color in pci_color_mapping.items():
        if pci_value in pci_range:
            pci_color = color
            break
    if pci_color == '000000':
        print("PCI value not in range!")
    return (pci_color) 
    


  
def plot_map_segment(gmap, segment_path):
    """
    Plot segment data on a Google Map.

    This function reads segment data from CSV files in the specified 'segment_path' and plots it on a Google Map
    using the provided 'gmap' object. It extracts the PCI (Pavement Condition Index) value and latitude/longitude
    coordinates to determine the color of the plotted segment on the map.

    Parameters:
    - gmap: gmaps.Map object
        The Google Map object to plot the segment data on.
    - segment_path (str):
        The path to the segment data files including PCI and latitude/longitude information.

    Note:
    - The function assumes that there are CSV files containing segment data in the specified 'segment_path'.
    - It reads the PCI value from the first CSV file and determines the color of the plotted segment based on PCI.
    - The latitude and longitude coordinates are extracted from a separate CSV file with '_lat_lon.csv' in its name.
    - The 'gmaps' library must be installed and configured with a valid API key to use this function.
    """
    df = pd.read_csv(glob.glob(os.path.join(segment_path, 'DJI_0*.csv'))[0])
    pci = df.iloc[0, 10]
    pci_color = get_pci_color(pci)

    df_report = pd.read_csv(glob.glob(os.path.join(segment_path, '*_lat_lon.csv'))[0])
    latitude_list = df_report['Latitude']
    longitude_list = df_report['Longitude']

    gmap.plot(latitude_list, longitude_list, edge_width=12, color=pci_color)




def create_graph(x_values , y_values , graph_para):
    """
    Create and save a bar graph based on the provided data.

    This function generates a bar graph using the given x and y values and saves it to the specified file path.
    
    Parameters:
    - x_values (list): The values for the x-axis (e.g., categories or labels).
    - y_values (list): The values for the y-axis (e.g., data points).
    - graph_para (dict): A dictionary containing graph parameters:
        - 'bar_color' (str): The color of the bars in the graph.
        - 'graph_title' (str): The title of the graph.
        - 'x_axis_label' (str): The label for the x-axis.
        - 'y_axis_label' (str): The label for the y-axis.
        - 'path' (str): The file path where the graph will be saved.

    Example:
    >>> x_values = ['Category A', 'Category B', 'Category C']
    >>> y_values = [10, 20, 15]
    >>> graph_parameters = {
    ...     'bar_color': 'blue',
    ...     'graph_title': 'Sample Bar Graph',
    ...     'x_axis_label': 'Categories',
    ...     'y_axis_label': 'Values',
    ...     'path': 'bar_graph.png'
    ... }
    >>> create_graph(x_values, y_values, graph_parameters)

    Note:
    - The 'bar_color' parameter specifies the color of the bars in the graph.
    - The 'graph_title' parameter sets the title of the graph.
    - The 'x_axis_label' parameter defines the label for the x-axis.
    - The 'y_axis_label' parameter defines the label for the y-axis.
    - The 'path' parameter specifies the file path (including the file name and extension) where the graph will be saved.
    """
    fig = plt.figure(figsize = (50, 10))
    ax = fig.add_subplot(1,1,1)
    ax.set_axisbelow(True)
    ax.patch.set_facecolor('white')
    ax.patch.set_alpha(1)
    
    # print(x_values[0])
    
    
    # plt.style.use('fivethirtyeight')
    plt.grid(True, color='black', linewidth=2, which='both', axis='y')
    plt.bar(x_values, y_values, width = 0.5, color=graph_para['bar_color'])
    
    # plt.title(graph_para['graph_title'], fontsize=50)
    # plt.xlabel(graph_para['x_axis_label'], fontsize=50,)
    plt.xticks(rotation =0 , fontsize=25)
    plt.yticks(fontsize=30)
    plt.ylabel(graph_para['y_axis_label'], fontsize=35)
    params = {'legend.fontsize': 'x-large',
            #  'figure.figsize': (15, 5),
            # 'axes.labelsize': 'x-large',
            # 'axes.titlesize':'x-large',
            # 'xtick.labelsize':'x-large',
            # 'ytick.labelsize':'x-large'
            }
    plt.rcParams.update(params)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    xlocs, xlabs = plt.xticks()
    for i, v in enumerate(y_values):
        if v != 0:
            vertical_distance_of_bar_label = max(y_values) / 10 * 0.07
            plt.text(xlocs[i], v + vertical_distance_of_bar_label, str(v), fontsize=35, fontweight='bold', horizontalalignment='center', color=graph_para['bar_color'])
    plt.savefig(graph_para['path'], dpi=200, bbox_inches='tight', facecolor='#ffffff')
    
    plt.close() 



def rank_similar_strings(list1: List[str], list2: List[str], similarity_metric='Levenshtein') -> List[Tuple[str, str, float]]:
    """
    Rank the similarity of strings in two lists.

    This function calculates the similarity between strings in 'list1' and 'list2' based on the specified
    similarity metric ('Levenshtein', 'Jaccard', or 'Cosine'). It returns a list of ranked pairs, each
    containing two strings and their similarity score.

    Parameters:
    - list1 (List[str]): The first list of strings for comparison.
    - list2 (List[str]): The second list of strings for comparison.
    - similarity_metric (str): The similarity metric to use for ranking (default is 'Levenshtein').

    Returns:
    List[Tuple[str, str, float]]: A list of ranked pairs, each containing two strings and their similarity score.

    Example:
    >>> list1 = ['apple', 'banana', 'cherry']
    >>> list2 = ['apple', 'orange', 'grape']
    >>> ranked_pairs = rank_similar_strings(list1, list2, similarity_metric='Jaccard')
    >>> print(ranked_pairs)

    Note:
    - Supported similarity metrics: 'Levenshtein', 'Jaccard', 'Cosine'.
    - The function uses Levenshtein distance for 'Levenshtein', Jaccard similarity for 'Jaccard',
      and Cosine similarity for 'Cosine'.
    - The result is a list of ranked pairs sorted by similarity score in descending order.
    """
    similarity_dict = {}
    for i, s1 in enumerate(list1):
        for j, s2 in enumerate(list2):
            if similarity_metric == 'Levenshtein':
                distance = Levenshtein.distance(s1, s2)
                similarity = 1 - distance / max(len(s1), len(s2))
            elif similarity_metric == 'Jaccard':
                set1 = set(s1.split())
                set2 = set(s2.split())
                similarity = len(set1.intersection(set2)) / len(set1.union(set2))
            elif similarity_metric == 'Cosine':
                vector1 = [s1.count(word) for word in set(s1.split())]
                vector2 = [s2.count(word) for word in set(s2.split())]
                dot_product = sum(i*j for i,j in zip(vector1, vector2))
                norm1 = sum(i**2 for i in vector1) ** 0.5
                norm2 = sum(i**2 for i in vector2) ** 0.5
                similarity = dot_product / (norm1 * norm2)
            else:
                raise ValueError("Invalid similarity metric. Valid options are 'Levenshtein', 'Jaccard', and 'Cosine'.")
            similarity_dict[(i, j)] = similarity

    sorted_pairs = sorted(similarity_dict, key=similarity_dict.get, reverse=True)
    ranked_pairs = [(list1[i], list2[j], similarity_dict[(i, j)]) for i, j in sorted_pairs]
    return ranked_pairs



def get_embed_links(service, folder_id): 
    """
    Get video embed links for videos in a Google Drive folder.

    This function queries a Google Drive folder using the provided Google Drive API 'service' and 'folder_id'
    to retrieve a list of video files with the MIME types 'video/mp4' and 'video/quicktime'. It then generates
    embed links for these video files and returns a list of video embed links.

    Parameters:
    - service: The Google Drive API service object for authentication.
    - folder_id (str): The ID of the Google Drive folder to search for videos.

    Returns:
    list of str: A list of video embed links.

    Note:
    - You need to set up the 'service' and obtain valid Google Drive API credentials before using this function.
    """
    
    page_token = None
    result = []
    while True:
        response = service.files().list(q="'{}' in parents".format(folder_id),
                                                spaces='drive',
                  
                                                fields='nextPageToken, files(id, name, mimeType)',
                                                pageToken=page_token).execute()
        for file in response.get('files', []):
            if file.get('mimeType')=='video/mp4':
                result.append(file)
            elif file.get('mimeType')=='video/quicktime':
                result.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    #generating embed item link for all videos
    preview_links = []
    for video in result:
        file_id = video['id']
        embed_link = 'https://drive.google.com/file/d/'+file_id+'/preview'
        preview_links.append(embed_link)
        
    # EMBEL LINK SAMPLE:
    # <iframe src="https://drive.google.com/file/d/13HBX11bAgfdEGDBTrgtP8ohLlmrDCeFw/preview" width="640" height="480" allow="autoplay"></iframe>

    videos_embed_links = []
    for item in preview_links:
        v_link = item
        videos_embed_links.append(v_link)
    return videos_embed_links


def get_folders(service, folder_id):
    """Get a list of all the subfolders within a specified folder.

    Args:
        service: The Drive API service object.
        folder_id: The ID of the parent folder.

    Returns:
        A list of dictionaries, each containing the ID and name of a subfolder.
    """
    folders = []
    query = "mimeType='application/vnd.google-apps.folder' and trashed = false and parents in '" + folder_id + "'"
    try:
        page_token = None
        while True:
            response = service.files().list(q = query,
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            folders.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
    except errors.HttpError as error:
        print(F'An error occurred: {error}')
        folders = None

    return folders



def Create_tem_count_area_file(file_path,
                               weather_condition,
                               survey_time,
                               survey_date):

    header = [
            
            #Crack Counts
            
            "Alligator count","Block count","Longitudinal count","Transverse count",           
            "Rutting count","Raveling count", "Corrugation count","Pothole count","Depression count","Edge cracking count",
            "Rail road crossing count","Bleeding count","Joint reflection count", "Patching count","Polished aggregate count", "Shoving count",
            "Slippage count", "Bumps and Sags count","Swell count", "Weathering count", 
            
            #Crack Area
            
            "Alligator area","Block area","Longitudinal area","Transverse area", "Rutting area", 
            "Raveling area","Corrugation area","Pothole area","Depression area","Edge cracking area",
            "Rail road crossing area","Bleeding area", "Joint reflection area","Patching area","Polished aggregate area", "Shoving area", 
            "Slippage area","Bumps and Sags area", "Swell area", "Weathering area",
            
            #Deduct values
            
            "Alligator DV", "Block DV","Longitudinal DV", "Transverse DV","Rutting DV",
            "Raveling DV", "Corrugation DV","Pothole DV", "Depression DV","Edge cracking DV", "Rail road crossing DV", 
            "Bleeding DV", "Joint Reflection DV","Patching DV","Polished aggregate DV","Shoving DV","Slippage DV","Bumps and Sags DV", 
            "Swell DV","Weathering DV",
            
            
            "Total DV","Corrected DV","PCI","Date","Time","Color Temp","Condition","Starting Latitude","Starting Longitude",
            "Ending Latitude","Ending Longitude"
            
            ]


    df = pd.read_csv(file_path)

    new_dict={}

    for indxx,name_txt in enumerate(header):
        
        if indxx < 20:
            new_dict[name_txt]=df.loc[indxx,"Counts"]
        if indxx > 19 and indxx < 40 :
            new_dict[name_txt]=df.loc[indxx-20,'Area']
        if indxx > 39 and indxx < 60 :
            new_dict[name_txt]=df.loc[indxx-40,"Deduct Values"]
            
        if 'Total DV' in name_txt:
            new_dict[name_txt]=df.loc[0,"Total DV"]
        if 'Corrected DV' in name_txt:
            new_dict[name_txt]=df.loc[0,"Corrected DV"]
        if 'PCI' in name_txt:
            new_dict[name_txt]=int(df.loc[0,"PCI"])
            
        if 'Total DV' in name_txt:
            new_dict[name_txt]=df.loc[0,"Total DV"]
            
        if 'Date' in name_txt:
            new_dict[name_txt]=survey_date
        
        if 'Time' in name_txt:
            new_dict[name_txt]=survey_time
        
        if 'Condition' in name_txt:
            new_dict[name_txt]=weather_condition
        
        

    # Convert dictionary to DataFrame
    df = pd.DataFrame([new_dict])
    
    file_dir = os.path.dirname(file_path)
    file_name= os.path.basename(file_path).split('.')[0]
    
    # Specify the CSV file path
    new_csv_file_path = os.path.join(file_dir, f"{file_name}_O_F.csv")

    # Write DataFrame to CSV file
    df.to_csv(new_csv_file_path, index=False)
    
    
    
    
def get_top_3_features(Full_database):

    # Identify the types of cracks with 'L', 'M', and 'H'
    cracks_with_levels = Full_database.columns[Full_database.columns.str.contains(r'\(L\)|\(M\)|\(H\)')]
    df_combined = Full_database.copy()

    # Drop the original columns with '(L)', '(M)', and '(H)'
    df_combined.drop(columns=cracks_with_levels, inplace=True)

    top_cracks = df_combined.sum(axis=0).sort_values(ascending=False).head(3)
    top_cracks_list = [crack.replace(' area', '') for crack in top_cracks.index]

    return top_cracks_list



def Create_tem_crack_area_file(new_formate_file,seg_name):
    
    cracks_names = ["Alligator ","Block","Longitudinal","Transverse", "Rutting","Raveling",
            "Corrugation","Pothole","Depression","Edge cracking","Rail road crossing","Bleeding", "Joint reflection",
            "Patching","Polished aggregate", "Shoving","Slippage","Bumps and Sags", "Swell", "Weathering"]
    header_list = cracks_names
    print("###################")
    datafram = pd.read_csv(new_formate_file)

    rows_list =[]
    detected_cracks=datafram['Name']
    detected_cracks_area=datafram['Area']




    for its_indx,each_crack_iter in enumerate(detected_cracks):
        rowInit=[0]*20
    
        for indxx,name_txt in enumerate(header_list):
            if each_crack_iter == name_txt.upper():
                rowInit[indxx]=detected_cracks_area[its_indx]  # assign the value of area to the corresponding column
                rows_list.append(rowInit)  # add the empty list to the main list

    # Specify the CSV file name
    file_dir = os.path.dirname(new_formate_file)
    
    # Specify the CSV file path
    new_csv_file_path = os.path.join(file_dir, f"DJI_{seg_name}_2_O_F.csv")

    # Write data to the CSV file with column names
    with open(new_csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header row with column names
        writer.writerow(header_list)
        
        # Write data rows
        writer.writerows(rows_list)
        
        

def extract_srt_data(srt_path):
    """
    Extracts data from an SRT file and returns it as a list of dictionaries.

    Args:
        srt_path (str): The path to the SRT file.

    Returns:
        list: A list of dictionaries containing the extracted data.
    """
    data = []
    with open(srt_path, "r") as srt:
        liness = srt.readlines()
        lines_count = 0        
        while lines_count < len(liness):
            packet = {} 
            group = [] # Each element of this list represent details of indvidual Frame
            done = False

            while not done:
                line = liness[lines_count]
                lines_count += 1
                

                if line.strip() == "": # means end of a frame
                    done = True
                    break
                else:
                    group.append(line)
                    
            time_date = group[3].strip().split(",")[0]
            date, timee = time_date.strip().split(" ")
            packet["time_stamp"] = timee
            packet["date"] = date
            
            linn_4 = group[4].strip().split("] [")
            for item in linn_4:
                if "longitude" in item:
                    packet["longitude"] = float(item.split(" ")[1])
                if "latitude" in item:
                    packet["latitude"] = float(item.split(" ")[-1])
                if "altitude" in item:
                    packet["altitude"] = float(item.split(" ")[1].replace("]", ""))
                if "iso" in item:
                    packet["iso"] = item.split(" ")[2]
                if "shutter" in item:
                    packet["shutter"] = item.split(" ")[2]
                if "ct" in item:
                    packet["ct"] = item.split(" ")[2].replace("]", "")
                    
            data.append(packet)
    return data





def generate_lat_lon_csv(segment_path, seg_file_num, data):
    """
    Generates a CSV file with latitude and longitude data from a list of dictionaries.

    Args:
    segment_path (str): The path to the segment directory.
    seg_file_num (str): The segment file number.
    data (list): A list of dictionaries containing latitude and longitude data.
    """
    csv_filename = os.path.join(segment_path, f"{seg_file_num}_lat_lon.csv")
    
    with open(csv_filename, "w+") as csv_file:
        csv_file.write("Latitude,Longitude\n")
        for packet in data:
            csv_file.write(f"{packet['latitude']},{packet['longitude']}\n")
            
    dfx = pd.read_csv(csv_filename)
    dfx.drop_duplicates().to_csv(csv_filename, index=False)      


import pandas as pd

def get_sum_data(MyList):
    """
    Calculates the total road segment length, total road length, and total cost from a list of road data.

    Args:
        MyList (list): A list containing road data where each element is a list representing a road segment.
                       Each road segment list should contain at least 5 elements: 
                       [segment_id, segment_length, total_segments_in_road, quality, cost]

    Returns:
        list: A list containing the total road data with the following format:
              [segment_id, total_segments_in_road, total_road_length, '', total_cost]
    """
    lengthofroad = 0
    totalroadsegment = 0
    totalCost = 0
    for i in range(len(MyList)):
        lengthofroad += MyList[i][2]
        totalroadsegment += MyList[i][1]
        totalCost += MyList[i][4]
    newList = [MyList[0][0], totalroadsegment, lengthofroad, '', totalCost]
    return newList



def get_roads_catagorization(roads_files_list,district_path,district_name):   
    """
    Categorizes road segments from a list of roads files and generates a summary of each category.
    The summary is saved to an Excel file.

    Args:
        roads_files_list (list): A list containing paths to Excel files, each representing a road category.

    Returns:
        None
    """
    good = []
    satisfactory = []
    fair = []
    poor = []
    verypoor = []
    serious = []
    failed = []
    extra = []
    
    for i in range(len(roads_files_list)):
        dfc = pd.read_excel(roads_files_list[i])
        dfc = dfc[:-1]
        good.append(dfc.iloc[0])
        satisfactory.append(dfc.iloc[1])
        fair.append(dfc.iloc[2])
        poor.append(dfc.iloc[3])
        verypoor.append(dfc.iloc[4])
        serious.append(dfc.iloc[5])
        failed.append(dfc.iloc[6])
        extra.append(dfc.iloc[7])
    
    allTypes = [good, satisfactory, fair, poor, verypoor, serious, failed, extra] 
    total_summ_list = []
    totalRoadLength = 0
    totalSegments = 0
    totalCost = 0
    
    for eachItem in allTypes:
        total_summ_list.append(get_sum_data(eachItem))
        totalRoadLength += get_sum_data(eachItem)[2]
        totalSegments += get_sum_data(eachItem)[1]
        totalCost += get_sum_data(eachItem)[4]
    
    totalRow = ['Total', totalSegments, round(totalRoadLength, 2), 100, round(totalCost, 2)]
   
    for i in range(len(total_summ_list)):
        if total_summ_list[i][2] == 0:
            total_summ_list[i][3] = 0
        else:
            total_summ_list[i][3] = round((total_summ_list[i][2] / totalRoadLength) * 100)  # percentage of roads with this quality
          
    total_summ_list.append(totalRow)
    total_summ_list = pd.DataFrame(total_summ_list)
    header = ['CONDITION', 'TOTAL SEGMENTS', 'TOTAL LENGTH (KM)', 'PERCENTAGE\n(LENGTH)', 'COST\n(MILLION/KM)']
    total_summ_list.columns = header

    dist_condition_file = district_path + os.sep + district_name + '_categorization.xlsx'
    total_summ_list.to_excel(dist_condition_file, index=False, header=True)
