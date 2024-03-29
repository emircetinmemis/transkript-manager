from    Utilities   import check_internet_connection, get_connection_details, download_chrome_driver, check_database_connection # -> Utility functions
from    Environment import EXECUTION_DC, SELENIUM_DC, ASCII_LOG, DEBUG # -> Environment variables
from    GUI         import TranscriptManager # -> DRIVER CODE
import  colorama # -> Colorful terminal
import  shutil # -> File operations
import  os # -> Path operations

# Init module variables
prints_enabled = True

def safe_start() -> None:
    """
    Method to start the application safely. It does checkout_pre_existing_checklist_must, checkout_pre_existing_checklist_relative, checkout_internet_connection, checkout_chrome_driver and checkout_database.
    @Parameters:
        None
    @Returns:
        None
    """
    if prints_enabled : print(colorama.Fore.MAGENTA, "Welcome to the \"Transcript Manager\" !\n", colorama.Fore.RESET)

    if prints_enabled : print(colorama.Fore.CYAN, "Starting application...\n |", colorama.Fore.RESET)

    def __checkout_pre_existing_checklist_must() -> None:
        """
        Method to checkout_pre_existing_checklist_must.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check for folders that must exist. If not, terminate the application.
        if prints_enabled : print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for required modules...", colorama.Fore.RESET)
        pre_existing_checklist_must_STATUS = []
        for current_folder_path in EXECUTION_DC.PRE_EXISTING_CHECKLIST_MUST :
            if not os.path.exists(current_folder_path) :
                pre_existing_checklist_must_STATUS.append(os.path.basename(current_folder_path))
        if pre_existing_checklist_must_STATUS :
            if prints_enabled : print(colorama.Fore.RED, ASCII_LOG["FAILURE"], f"The following modules are missing -> {pre_existing_checklist_must_STATUS}", colorama.Fore.RESET)
            exit()
        else :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"All required modules approved -> {[os.path.basename(fname) for fname in EXECUTION_DC.PRE_EXISTING_CHECKLIST_MUST]}", colorama.Fore.RESET)

    def __checkout_pre_existing_checklist_relative() -> None:
        """
        Method to checkout_pre_existing_checklist_relative.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check for folders that should exist. If not, create them. If yes, clean them.
        if prints_enabled : print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for relative packs...", colorama.Fore.RESET)
        pre_existing_checklist_relative_STATUS = []
        for current_folder_path in EXECUTION_DC.PRE_EXISTING_CHECKLIST_RELATIVE :
            if not os.path.exists(current_folder_path) :
                pre_existing_checklist_relative_STATUS.append(os.path.basename(current_folder_path))
                os.mkdir(current_folder_path)
        if pre_existing_checklist_relative_STATUS :
            if prints_enabled : print(colorama.Fore.BLUE, ASCII_LOG["SUCCESS"], f"The following packs created -> {pre_existing_checklist_relative_STATUS}", colorama.Fore.RESET)
        else :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"All relative packs approved -> {[os.path.basename(fname) for fname in EXECUTION_DC.PRE_EXISTING_CHECKLIST_RELATIVE]}", colorama.Fore.RESET)
    
    def __checkout_internet_connection() -> None:
        """
        Method to checkout_internet_connection.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check for internet connection. If not, terminate the application.
        if prints_enabled : print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for internet connection...", colorama.Fore.RESET)    
        retrieval = check_internet_connection()
        if retrieval : 
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"Internet connection established -> {get_connection_details()}", colorama.Fore.RESET)
        else :
            if prints_enabled : print(colorama.Fore.RED, ASCII_LOG["ERROR"], f"Internet connection failrue", colorama.Fore.RESET)
            exit()

    def __checkout_chrome_driver() -> None:
        """
        Method to checkout_chrome_driver.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check for chrome driver. If not, download it.
        if prints_enabled : print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for chrome driver...", colorama.Fore.RESET)
        if not os.path.exists(SELENIUM_DC.CHROME_DRIVER_PATH) :
            if prints_enabled : print(colorama.Fore.BLUE, ASCII_LOG["SUCCESS"], f"Chrome driver not found. Downloading...", colorama.Fore.RESET)
            is_download_successfull, message = download_chrome_driver()
            if is_download_successfull :
                if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"Chrome driver downloaded successfully -> {message}", colorama.Fore.RESET)
            else :
                if prints_enabled : print(colorama.Fore.RED, ASCII_LOG["FAILURE"], f"Chrome driver download failed -> {message}", colorama.Fore.RESET)
                exit()
        else :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"Chrome driver found -> {SELENIUM_DC.CHROME_DRIVER_PATH}", colorama.Fore.RESET)

    def __checkout_database() -> None:
        """
        Method to checkout_database.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check if mongoDB is reachable. If not, terminate the application.
        if prints_enabled : print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for database connection...", colorama.Fore.RESET)
        is_database_connection_successfull, message = check_database_connection()
        if is_database_connection_successfull :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"Database connection established -> {message}", colorama.Fore.RESET)
        else :
            if prints_enabled : print(colorama.Fore.RED, ASCII_LOG["ERROR"], f"Database connection failure -> {message}", colorama.Fore.RESET)
            exit()

    def __checkout_post_cleanup_list() -> None:
        """
        Method to checkout_post_cleanup_list.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check for folders that should be cleaned. If yes, clean them.
        if prints_enabled : print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Cleaning temp folders...", colorama.Fore.RESET)
        post_cleanup_list_STATUS = []
        for current_folder_path in EXECUTION_DC.POST_CLEANUP_LIST :
            if os.path.exists(current_folder_path) :
                post_cleanup_list_STATUS.append(os.path.basename(current_folder_path))
                shutil.rmtree(current_folder_path)
        if post_cleanup_list_STATUS :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"The following folders cleaned -> {post_cleanup_list_STATUS}", colorama.Fore.RESET)
        else :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"All folders \"clean_approved\" -> {[os.path.basename(fname) for fname in EXECUTION_DC.POST_CLEANUP_LIST]}", colorama.Fore.RESET)

    # Call all checkout methods in order
    try :
        __checkout_post_cleanup_list()
    except PermissionError as e:
        # This error occurs when the application is running in background and the user tries to delete the folder manually.
        # In this case, the application will terminate without deleting the folder.
        pass
    __checkout_pre_existing_checklist_must()
    __checkout_pre_existing_checklist_relative()
    __checkout_internet_connection()
    __checkout_chrome_driver()
    __checkout_database()

def safe_execute() -> None:
    """
    Method to safe_execute. It call the Driver Code inside handlers, for any stat it can directly terminate and restart the application.
    @Parameters:
        None
    @Returns:
        None
    """

    if prints_enabled : print(colorama.Fore.LIGHTCYAN_EX, "\n Executing application...\n |", colorama.Fore.RESET)

    try :
        # Call the mainloop() of TranscriptManager
        TranscriptManager(DEBUG=DEBUG).mainloop()
        run_status = "successfully"
    except Exception as e:
        run_status = "ineffectively"
        print(colorama.Fore.LIGHTRED_EX, colorama.Back.WHITE, ASCII_LOG["ERROR"], f"An error occured -> {e}", colorama.Fore.RESET, colorama.Back.RESET)

    if prints_enabled : print(colorama.Fore.LIGHTCYAN_EX, f"Application executed {run_status}", colorama.Fore.RESET)

def safe_end() -> None:
    """
    Method to safe_end. It does checkout_post_cache_cleanup_list and checkout_post_cleanup_list.
    @Parameters:
        None
    @Returns:
        None
    """
    if prints_enabled : print(colorama.Fore.CYAN, "\n Terminating application...\n |", colorama.Fore.RESET)

    def __checkout_post_cache_cleanup_list() -> None:
        """
        Method to checkout_post_cache_cleanup_list.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check for folders that includes cache files. If yes, clean them.
        if prints_enabled : print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Cleaning cache files...", colorama.Fore.RESET)
        post_cache_cleanup_list_STATUS = []
        for current_folder_path in EXECUTION_DC.POST_CACHE_CLEANUP_LIST :
            # check if there is "__pycache__" folder
            possible_pycache_folder_path = os.path.join(current_folder_path, "__pycache__")
            if os.path.exists(possible_pycache_folder_path) :
                post_cache_cleanup_list_STATUS.append(os.path.basename(current_folder_path))
                shutil.rmtree(possible_pycache_folder_path)
        if post_cache_cleanup_list_STATUS :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"The following folder's caches cleaned -> {post_cache_cleanup_list_STATUS}", colorama.Fore.RESET)
        else :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"All folders \"cache_approved\" -> {[os.path.basename(fname) for fname in EXECUTION_DC.POST_CACHE_CLEANUP_LIST]}", colorama.Fore.RESET)
    
    def __checkout_post_cleanup_list() -> None:
        """
        Method to checkout_post_cleanup_list.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check for folders that should be cleaned. If yes, clean them.
        if prints_enabled : print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Cleaning temp folders...", colorama.Fore.RESET)
        post_cleanup_list_STATUS = []
        for current_folder_path in EXECUTION_DC.POST_CLEANUP_LIST :
            if os.path.exists(current_folder_path) :
                post_cleanup_list_STATUS.append(os.path.basename(current_folder_path))
                shutil.rmtree(current_folder_path)
        if post_cleanup_list_STATUS :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"The following folders cleaned -> {post_cleanup_list_STATUS}", colorama.Fore.RESET)
        else :
            if prints_enabled : print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"All folders \"clean_approved\" -> {[os.path.basename(fname) for fname in EXECUTION_DC.POST_CLEANUP_LIST]}", colorama.Fore.RESET)

    # Call all checkout methods in order
    __checkout_post_cache_cleanup_list()
    try :
        __checkout_post_cleanup_list()
    except PermissionError as e:
        # This error occurs when the application is running in background and the user tries to delete the folder manually.
        # In this case, the application will terminate without deleting the folder.
        pass

    if prints_enabled : print(colorama.Fore.MAGENTA, "\n Application terminated successfully", colorama.Fore.RESET)
