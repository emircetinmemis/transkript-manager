from tkinter.ttk import Treeview, Style # -> GUI
from Environment import GUI_DC # -> Environment Variables
from Utilities import ( # -> Utility functions
    calculate_performance, # -> Calculate performance of a course list
    subtract_course, # -> Subtract a course from a course list
    update_course, # -> Update a course in a course list
    add_course, # -> Add a course to a course list
    filter_by, # -> Filter a course list by a key
    sort_by, # -> Sort a course list by a key
)
from GUI import ( # -> Service frames
    FilterSelecter, # -> Filter selecter service
    CourseRemover, # -> Course remover service
    CourseUpdater, # -> Course updater service
    CourseAdder, # -> Course adder service
)
import customtkinter as ctk # -> GUI

class GradeUpdater(ctk.CTkFrame) :

    def __init__(self, application_container : ctk.CTkFrame, parent : ctk.CTkFrame, root : ctk.CTk, current_user_data : dict, DEBUG : bool = False, *args, **kwargs) -> None:
        """
        Constructor method for GradeUpdater class. Used to initialize main window of the program.
        @Parameters:
            application_container - Required : Container frame of the application. (ttk.Frame) -> Which is used to place the application frame.
            parent                - Required : Parent frame of the application. (ttk.Frame) -> Which is used to set connection to application frame.
            root                  - Required : Root window of the application. (tk.Tk) -> Which is used to set connection between frames.
            current_user_data     - Required : Current user data. (dict) -> Which is used to determine current user data.
            DEBUG                 - Optional : Debug mode flag. (bool) (default : False) -> Which is used to determine whether the application is in debug mode or not.
        @Returns:
            None
        """
        # Initialize main window of program
        super().__init__(application_container, *args, **kwargs)

        # Set class variables
        self.application_container = application_container
        self.parent = parent
        self.root   = root
        self.DEBUG  = DEBUG
        
        # Set program variables
        self.possibleNotations = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "I", "W", "S"]
        self.weights = {"A":4.00, "A-":3.70, "B+":3.30, "B":3.00, "B-":2.70, "C+":2.30, "C":2.00, "C-":1.70, "D+":1.30, "D":1.00, "F":0.00, "I":0.00, "W":0.00, "S":0.00}
        self.possibleCredits = [1, 2, 3, 4, 5, 6, 7]
        
        # Load initial data
        self.__load_user_data(current_user_data)
        self.__load_output_info(is_init=True)
        self.__update_user_data()

        # Load main containers
        self.__load_containers()

        # Load main frames
        self.__load_program_buttons()
        self.__load_program_display()
        self.__load_program_output()

    def __load_containers(self) -> None:
        """
        Loads main containers into class fields.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the initial configuration, to make expandable affect on window.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Set main container.
        self.container = ctk.CTkFrame(self, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Configure main container.
        self.container.grid_rowconfigure((0,1,2), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Set sub containers.
        self.program_buttons_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.program_buttons_container.grid(row=0, column=0, sticky="nsew")

        self.program_display_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.program_display_container.grid(row=1, column=0, sticky="nsew", pady=GUI_DC.GENERAL_PADDING*1.5)

        self.program_output_container  = ctk.CTkFrame(self.container, fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.program_output_container.grid(row=2, column=0, sticky="nsew")


    def __load_program_buttons(self) -> None:
        """
        Loads program buttons to container.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure program buttons container.
        self.program_buttons_container.grid_rowconfigure((0), weight=1)
        self.program_buttons_container.grid_columnconfigure((0,1,2,3), weight=1)

        # Create program buttons. & Configure them. & Place them.
        self.filter_button = ctk.CTkButton(self.program_buttons_container, text=self._get_text("Filter Courses"), command=self.__filter,
            fg_color = GUI_DC.BUTTON_LIGHT_PINK,
            hover_color = GUI_DC.BUTTON_LIGHT_PINK_HOVER,
        )
        self.filter_button.grid(row=0, column=0)

        self.update_course_button = ctk.CTkButton(self.program_buttons_container, text=self._get_text("Update Course"), command=self.__update_course,
            fg_color = GUI_DC.BUTTON_LIGHT_BLUE,
            hover_color = GUI_DC.BUTTON_LIGHT_BLUE_HOVER,
        )
        self.update_course_button.grid(row=0, column=1)

        self.add_course_button = ctk.CTkButton(self.program_buttons_container, text=self._get_text("Add Course"), command=self.__add_course,
            fg_color = GUI_DC.BUTTON_LIGHT_ORANGE,
            hover_color = GUI_DC.BUTTON_LIGHT_ORANGE_HOVER,
        )
        self.add_course_button.grid(row=0, column=2)

        self.remove_course_button = ctk.CTkButton(self.program_buttons_container, text=self._get_text("Remove Course"), command=self.__remove_course,
            fg_color = GUI_DC.BUTTON_LIGHT_PURPLE,
            hover_color = GUI_DC.BUTTON_LIGHT_PURPLE_HOVER,
        )
        self.remove_course_button.grid(row=0, column=3)

        for current_button in self.program_buttons_container.winfo_children() :
            current_button.configure(
                bg_color=GUI_DC.DARK_BACKGROUND,
                corner_radius=25,
                text_color=GUI_DC.LIGHT_TEXT_COLOR,
                text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
                font=("Arial", 12, "bold"),
                height=0,
            )
            current_button.grid_configure(padx=GUI_DC.GENERAL_PADDING, sticky="nsew")

    def __load_program_display(self) -> None:
        """
        Loads program display to container.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure program display container.
        #self.program_display_container.grid_columnconfigure((0,1), weight=1)
        #self.program_display_container.grid_rowconfigure((0), weight=1)

        # Set a scrollbar for treeview.
        self.treeview_scrollbar1 = ctk.CTkScrollbar(self.program_display_container, orientation="vertical", 
            bg_color=GUI_DC.DARK_BACKGROUND, 
            fg_color=GUI_DC.DARK_BACKGROUND,
            button_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
            button_hover_color=GUI_DC.MEDIUM_TEXT_COLOR,
        )
        #self.treeview_scrollbar.grid(row=0, column=1, sticky="nse", padx=10, pady=10)
        self.treeview_scrollbar1.pack(side="right", fill="y", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.GENERAL_PADDING)

        # Set a style for tkinter treeview.
        self.treeview_scrollbar2 = ctk.CTkScrollbar(self.program_display_container, orientation="vertical",
            bg_color=GUI_DC.DARK_BACKGROUND,
            fg_color=GUI_DC.DARK_BACKGROUND,
            button_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
            button_hover_color=GUI_DC.MEDIUM_TEXT_COLOR,
        )
        self.treeview_scrollbar2.pack(side="left", fill="y", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.GENERAL_PADDING)

        # Set up a specific theme for the table. Currenty CTK Doesn't have Treeview widget.
        self.style_for_treeview = Style()
        self.style_for_treeview.theme_use("default")
        self.style_for_treeview.configure("Treeview", 
            background=GUI_DC.SECONDARY_DARK_BACKGROUND,
            fieldbackground=GUI_DC.SECONDARY_DARK_BACKGROUND, # When there are less rows than the height of the treeview, this color will be used to fill the rest of the space.
            foreground=GUI_DC.LIGHT_TEXT_COLOR,
            rowheight = 43,
            font=("Arial", 14, "italic"),
            borderwidth=2,
            bordercolor="red",
        )
        self.style_for_treeview.map("Treeview",
            background=[("selected", GUI_DC.DARK_BACKGROUND)],
            foreground=[("selected", GUI_DC.LIGHT_TEXT_COLOR)],
        )
        self.style_for_treeview.configure("Treeview.Heading", 
            background=GUI_DC.DARK_BACKGROUND,
            fieldbackground=GUI_DC.DARK_BACKGROUND, # When there are less rows than the height of the treeview, this color will be used to fill the rest of the space.
            foreground=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 16, "bold"),
        )
        self.style_for_treeview.map("Treeview.Heading",
            background=[("active", GUI_DC.SECONDARY_DARK_BACKGROUND), ("!disabled", GUI_DC.DARK_BACKGROUND), ("pressed", "red")],
        )

        # Openup main treeview table.
        self.display_treeview = Treeview(self.program_display_container, show="headings", selectmode="browse", yscrollcommand=self.treeview_scrollbar1.set, cursor="hand2")
        #self.display_treeview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.display_treeview.pack(side="left", fill="both", expand=True, pady=GUI_DC.GENERAL_PADDING)
        # Configure scrollbar.
        self.treeview_scrollbar1.configure(command=self.display_treeview.yview)
        self.treeview_scrollbar2.configure(command=self.display_treeview.yview)

        # Set columns
        self.display_treeview["columns"] = ("_code", "_name", "_language", "_credit", "_grade", "_grade_point")

        # This map is used to store the sorting history of the columns. EXMP: Double click on a sort button will reverse the sorting order.
        self.sorting_reverse_history = {
            "course_code" : False,
            "course_name" : False,
            "course_lang" : False,
            "course_credit" : False,
            "course_grade" : False,
            "course_grade_point" : False
        }
        # Configure headings.
        self.display_treeview.heading("_code", text=self._get_text("Course Code"), command=lambda : self.__sort("course_code"))
        self.display_treeview.heading("_name", text=self._get_text("Course Name"), command=lambda : self.__sort("course_name"))
        self.display_treeview.heading("_language", text=self._get_text("Course Language"), command=lambda : self.__sort("course_lang"))
        self.display_treeview.heading("_credit", text=self._get_text("Course Credit"), command=lambda : self.__sort("course_credit"))
        self.display_treeview.heading("_grade", text=self._get_text("Course Grade"), command=lambda : self.__sort("course_grade"))
        self.display_treeview.heading("_grade_point", text=self._get_text("Course Grade Point"), command=lambda : self.__sort("course_grade_point"))

        # Configure columns.
        self.display_treeview.column("_code", anchor="center")
        self.display_treeview.column("_name", anchor="center", width=400)
        self.display_treeview.column("_language", anchor="center")
        self.display_treeview.column("_credit", anchor="center")
        self.display_treeview.column("_grade", anchor="center")
        self.display_treeview.column("_grade_point", anchor="center")

        # Init Load call -> clean & insert data into treeview.
        self.__update_program_display()
        
    def __load_program_output(self) -> None:
        """
        Loads program output to container.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure program output container.
        self.program_output_container.grid_rowconfigure((0,1), weight=1)
        self.program_output_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Set feature variables.
        self.modes = ["BOTH", "MODIFIED"]
        self.output_mode = "BOTH"

        # Set class variables.
        self.credits_attempted_output_text = ctk.StringVar()
        self.credits_successful_output_text = ctk.StringVar()
        self.credits_included_in_gpa_output_text = ctk.StringVar()
        self.gpa_output_text = ctk.StringVar()
        
        # One init call -> it gets the data from the course list and updates the output labels.
        self.__update_output_label()
        
        # Create output labels. & Set them to the container. & Place them.
        self.credits_attempted_info_label = ctk.CTkLabel(self.program_output_container, text=self._get_text("Credits Attempted"),
            text_color=GUI_DC.BUTTON_LIGHT_YELLOW,
        )
        self.credits_attempted_info_label.grid(row=0, column=0, sticky="nsew")
        self.credits_attempted_output_label = ctk.CTkLabel(self.program_output_container, textvariable=self.credits_attempted_output_text,
            text_color=GUI_DC.BUTTON_LIGHT_YELLOW_HOVER,
        )
        self.credits_attempted_output_label.grid(row=1, column=0, sticky="nsew")

        self.credits_successful_info_label = ctk.CTkLabel(self.program_output_container, text=self._get_text("Credits Successful"),
            text_color=GUI_DC.BUTTON_LIGHT_YELLOW,
        )
        self.credits_successful_info_label.grid(row=0, column=1, sticky="nsew")
        self.credits_successful_output_label = ctk.CTkLabel(self.program_output_container, textvariable=self.credits_successful_output_text,
            text_color=GUI_DC.BUTTON_LIGHT_YELLOW_HOVER,
        )
        self.credits_successful_output_label.grid(row=1, column=1, sticky="nsew")

        self.credits_included_in_gpa_info_label = ctk.CTkLabel(self.program_output_container, text=self._get_text("Credits Included in GPA"),
            text_color=GUI_DC.BUTTON_LIGHT_YELLOW,
        )
        self.credits_included_in_gpa_info_label.grid(row=0, column=2, sticky="nsew")
        self.credits_included_in_gpa_output_label = ctk.CTkLabel(self.program_output_container, textvariable=self.credits_included_in_gpa_output_text,
            text_color=GUI_DC.BUTTON_LIGHT_YELLOW_HOVER,
        )
        self.credits_included_in_gpa_output_label.grid(row=1, column=2, sticky="nsew")

        self.gpa_info_label = ctk.CTkLabel(self.program_output_container, text=self._get_text("GPA"),
            text_color=GUI_DC.BUTTON_LIGHT_YELLOW,
        )
        self.gpa_info_label.grid(row=0, column=3, sticky="nsew")
        self.gpa_output_label = ctk.CTkLabel(self.program_output_container, textvariable=self.gpa_output_text,
            text_color=GUI_DC.BUTTON_LIGHT_YELLOW_HOVER,
        )
        self.gpa_output_label.grid(row=1, column=3, sticky="nsew")

        # Bind events. For each button in the container, bind the event to the switch output mode function. To make easier to click.
        for widget in self.program_output_container.winfo_children() :
            widget.bind("<Button-1>", self.__switch_output_mode)
            widget.configure(
                font=("Arial", 12, "bold"),
                anchor="center",
                corner_radius=0,
                height=0,
            )
            widget.grid_configure(padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        # Bind the whole container to the switch output mode function. To make easier to click.
        self.program_output_container.bind("<Button-1>", self.__switch_output_mode)

        # An post_init call self.__update_output_label() to colorize labels.
        self.__update_output_label()


    def __update_user_data(self) -> None:
        """
        Wraps the parent's update_user_data method. And updates changed data on ApplicationFrame by doing a bridge.
        @Parameters:
            None
        @Returns:
            None
        """
        # Update user data on ApplicationFrame
        self.parent.update_user_data(self.__create_user_data())

    def __load_user_data(self, given_user_data : dict) -> None:
        """
        Loads user data into class fields. Does pre-processing on user data, turns None values into default values. (Because GradeUpdater program is the initial prgoram!)
        @Parameters:
            given_user_data - Required : Given user data. (dict) -> Which is used to load user data into class fields.
        @Returns:
            None
        """
        # Load user data into class fields. Check for None values and turn them into default values.
        self.owner_id : str = given_user_data["owner_id"]
        self.parsing_type : str = given_user_data["parsing_type"]
        self.parsing_language : str = given_user_data["parsing_language"]
        self.transcript_manager_date : str = given_user_data["transcript_manager_date"]
        self.transcript_creation_date : str = given_user_data["transcript_creation_date"]
        self.semesters : dict = given_user_data["semesters"]
        self.original_course_list : list = given_user_data["original_course_list"]
        self.filtering : list = given_user_data["filtering"] or []
        self.sorting : dict = given_user_data["sorting"] or {"sort_key" : None, "should_reverse" : None}
        self.modified_course_list : list = given_user_data["modified_course_list"]  or self.original_course_list.copy()
        self.document_name : str = given_user_data["document_name"]
        self.updated_course_list : list = given_user_data["updated_course_list"] or []
        self.subtracted_course_list : list = given_user_data["subtracted_course_list"] or []
        self.added_course_list : list = given_user_data["added_course_list"] or []

    def __load_output_info(self, is_init : bool = False) -> None:
        """
        Loads output info into class fields.
        @Parameters:
            is_init - Optional : Initialization flag. (bool) (default : False) -> Which is used to determine whether the program is in initialization phase or not.
        @Returns:
            None
        """

        # If on init, load te original performance data too.
        if is_init :
            original_performance = calculate_performance(self.original_course_list)
            self.original_credits_attempted = ctk.IntVar(value=original_performance["credits_attempted"])
            self.original_credits_successful = ctk.IntVar(value=original_performance["credits_successful"])
            self.original_credits_included_in_gpa = ctk.IntVar(value=original_performance["credits_included_in_gpa"])
            self.original_gpa = ctk.DoubleVar(value=original_performance["gpa"])
        
        # Load modified performance data.
        modified_performance = calculate_performance(self.modified_course_list)
        self.modified_credits_attempted = ctk.IntVar(value=modified_performance["credits_attempted"])
        self.modified_credits_successful = ctk.IntVar(value=modified_performance["credits_successful"])
        self.modified_credits_included_in_gpa = ctk.IntVar(value=modified_performance["credits_included_in_gpa"])
        self.modified_gpa = ctk.DoubleVar(value=modified_performance["gpa"])

    def __create_user_data(self) -> dict:
        """
        Creates user data from class fields.
        @Parameters:
            None
        @Returns:
            new_document - Required : New user data. (dict)
        """
        # Create new user data from class fields.
        new_document = {
            "owner_id" : self.owner_id,
            "parsing_type" : self.parsing_type,
            "parsing_language" : self.parsing_language,
            "transcript_manager_date" : self.transcript_manager_date,
            "transcript_creation_date" : self.transcript_creation_date,
            "semesters" : self.semesters,
            "original_course_list" : self.original_course_list,
            "filtering" : self.filtering,
            "sorting" : self.sorting,
            "modified_course_list" : self.modified_course_list,
            "document_name" : self.document_name,
            "updated_course_list" : self.updated_course_list,
            "subtracted_course_list" : self.subtracted_course_list,
            "added_course_list" : self.added_course_list
        }
        # Return new user data.
        return new_document

    def _get_text(self, text : str) -> str:
        """
        Gets the text from the language dictionary.
        @Parameters:
            text - Required : Text to get from the dictionary. (str) -> Which is used to get the text from the language dictionary for translation.
        @Return:
            translated_text - str : Translated text. (str)
        """
        # Direct wrapper to parent's _get_text method.
        return self.parent._get_text(text, self.parsing_language)


    def __update_program_display(self) -> None:
        """
        Updates program display. Clears all data and inserts new data. This refreshes the display.
        @Parameters:
            None
        @Returns:
            None
        """
        # Clear all data
        self.display_treeview.delete(*self.display_treeview.get_children())

        # Get updated course codes to tick updated courses.
        updated_course_codes = [course["course_code"] for course in self.updated_course_list]

        # Get added course codes to tick added courses.
        added_course_codes = [course["course_code"] for course in self.added_course_list]

        # Add current data
        for course in self.modified_course_list :
            if course["course_code"] in updated_course_codes :
                self.display_treeview.insert("", "end", values=(course["course_code"], course["course_name"], course["course_lang"], course["course_credit"], course["course_grade"], course["course_grade_point"]), tags=("updated",))
            elif course["course_code"] in added_course_codes :
                self.display_treeview.insert("", "end", values=(course["course_code"], course["course_name"], course["course_lang"], course["course_credit"], course["course_grade"], course["course_grade_point"]), tags=("added",))
            else :
                self.display_treeview.insert("", "end", values=(course["course_code"], course["course_name"], course["course_lang"], course["course_credit"], course["course_grade"], course["course_grade_point"]))
        
        # Make updated courses highlighted.
        self.display_treeview.tag_configure("updated", background=GUI_DC.BUTTON_LIGHT_BLUE_HOVER, foreground=GUI_DC.DARK_TEXT_COLOR)

        # Make added courses highlighted.
        self.display_treeview.tag_configure("added", background=GUI_DC.BUTTON_LIGHT_ORANGE_HOVER, foreground=GUI_DC.DARK_TEXT_COLOR)
    
    def __switch_output_mode(self, *args, **kwargs) -> None:
        """
        Switches output mode. If the output mode is BOTH, it switches to MODIFIED. If the output mode is MODIFIED, it switches to BOTH.
        @Parameters:
            event - Required : Event object. (tk.Event) -> It is used to get the widget that is clicked.
        @Returns:
            None
        """
        # Switch output mode.
        if self.output_mode == "BOTH" :
            self.output_mode = "MODIFIED"
        else :
            self.output_mode = "BOTH"
        # Call-Back -> Update output labels. -> This is done to update the output labels with the new output mode.
        self.__update_output_label()

    def __update_output_label(self) -> None:
        """
        Updates output labels. It gets the data from the course list and updates the output labels.
        @Parameters:
            None
        @Returns:
            None
        """
        def ____reconfigure_output_text(modified : ctk.StringVar, original : ctk.StringVar = None) -> str:
            """
            Reconfigures output text. It gets the data from the course list and updates the output labels. If only 1 parameter passes, than it doesn texarize the output text. It onyl returns the value.
            # Parameters:
                modified - Required : Modified value. (tk.StringVar) -> It is the value that is going to be displayed.
                original - Optional : Original value. (tk.StringVar) -> It is the value that is going to be displayed. If it is None, than it is not displayed.
            # Returns:
                str : Output text. (str) -> It is the output text that is going to be displayed.
            """
            # If original is None, than it is not displayed.
            if original is None :
                return modified.get()
            else :
                # If original is not None, than it is displayed. With an arrow in the middle.
                return "{} {} {}".format(original.get(), "\u279C", modified.get())
        
        # If output mode is BOTH, than it displays both original and modified values. If it is MODIFIED, than it displays only modified values.
        if self.output_mode == "BOTH" :
            # Get data from course list. Than update output labels by resetting tk.StringVar objects.
            self.credits_attempted_output_text.set(____reconfigure_output_text(self.modified_credits_attempted, self.original_credits_attempted))
            self.credits_successful_output_text.set(____reconfigure_output_text(self.modified_credits_successful, self.original_credits_successful))
            self.credits_included_in_gpa_output_text.set(____reconfigure_output_text(self.modified_credits_included_in_gpa, self.original_credits_included_in_gpa))
            self.gpa_output_text.set(____reconfigure_output_text(self.modified_gpa, self.original_gpa))
        elif self.output_mode == "MODIFIED" :
            # Get data from course list. Than update output labels by resetting tk.StringVar objects.
            self.credits_attempted_output_text.set(____reconfigure_output_text(self.modified_credits_attempted))
            self.credits_successful_output_text.set(____reconfigure_output_text(self.modified_credits_successful))
            self.credits_included_in_gpa_output_text.set(____reconfigure_output_text(self.modified_credits_included_in_gpa))
            self.gpa_output_text.set(____reconfigure_output_text(self.modified_gpa))

        label_color_map = {
            "increase" : GUI_DC.BUTTON_LIGHT_GREEN_HOVER,
            "decrease" : GUI_DC.BUTTON_LIGHT_RED_HOVER,
            "neutral" : GUI_DC.BUTTON_LIGHT_YELLOW_HOVER
        }
        get_stat = lambda modified_value_str_var, original_value_str_var : "increase" if float(modified_value_str_var.get()) > float(original_value_str_var.get()) else "decrease" if float(modified_value_str_var.get()) < float(original_value_str_var.get()) else "neutral"

        # Update output label colors.
        try :
            self.credits_attempted_output_label.configure(text_color=label_color_map[get_stat(self.modified_credits_attempted, self.original_credits_attempted)])
            self.credits_successful_output_label.configure(text_color=label_color_map[get_stat(self.modified_credits_successful, self.original_credits_successful)])
            self.credits_included_in_gpa_output_label.configure(text_color=label_color_map[get_stat(self.modified_credits_included_in_gpa, self.original_credits_included_in_gpa)])
            self.gpa_output_label.configure(text_color=label_color_map[get_stat(self.modified_gpa, self.original_gpa)])
        except AttributeError :
            # This means, it is not initialized yet. So, it is not updated.
            pass

    def ___update_program(self) -> None:
        """
        Updates Program by;
            Shared Variables
            Output Info 
            Program Display
        @Parameters:
            None
        @Returns:
            None
        """
        # Call update functions -> To take new operations to affect.
        self.__update_user_data()
        self.__load_output_info()
        self.__update_output_label()
        self.__update_program_display()


    def __filter(self) -> None:
        """
        Filters course list. It filters the course list by the selected filterings.
        @Parameters:
            None
        @Returns:
            None
        """    
        # Disable filter button to prevent multiple filtering button handle.
        self.filter_button.configure(text=self._get_text("Filtering"), state="disabled")

        # Set feature variables.
        available_filterings = {"course_lang" : [], "course_credit" : [], "course_grade" : [], "course_grade_point" : []}
        available_filterings_text_display = {self._get_text("Language") : "course_lang", self._get_text("Credit") : "course_credit", self._get_text("Grade") : "course_grade", self._get_text("Grade Point"): "course_grade_point"}

        # Fill feature variables.
        for course in self.modified_course_list :
            current_course_lang = course["course_lang"]
            current_course_credit = course["course_credit"]
            current_course_grade = course["course_grade"]
            current_course_grade_point = course["course_grade_point"]

            if current_course_lang not in available_filterings["course_lang"] :
                available_filterings["course_lang"].append(current_course_lang)
            if current_course_credit not in available_filterings["course_credit"] :
                available_filterings["course_credit"].append(current_course_credit)
            if current_course_grade not in available_filterings["course_grade"] :
                available_filterings["course_grade"].append(current_course_grade)
            if current_course_grade_point not in available_filterings["course_grade_point"] :
                available_filterings["course_grade_point"].append(current_course_grade_point)

        # Sort feature variables. -> It is done to make the filter selecter look better.
        for key in available_filterings :
            current_value_list = available_filterings[key]
            # if key is "course_grade_point", make every element is float, then sort, and then convert back to string
            if key == "course_grade_point" :
                current_value_list = [float(value) for value in current_value_list]
                current_value_list.sort()
                current_value_list = [str(value) for value in current_value_list]
            else :
                # If key is not "course_grade_point", than sort normally.
                current_value_list.sort()
            # Update available_filterings.
            available_filterings[key] = current_value_list

        # Get a copy of filtering.
        previous_filtering = self.filtering.copy()

        # Ask user to select filterings.
        obj = FilterSelecter(self, self.filtering, available_filterings, available_filterings_text_display, self.parsing_language)
        self.filtering = obj.get_result()

        # Get a copy of new filtering.
        current_filtering = self.filtering.copy()

        # Compare two filtering values, when change detected, rescale the whole course list to avoid data loss & bugs.
        if previous_filtering != current_filtering :
            self.modified_course_list = self.original_course_list.copy()

            # Apply operations by one by.
            for course in self.added_course_list :
                self.modified_course_list = add_course(self.modified_course_list, course)
            for course in self.subtracted_course_list :
                self.modified_course_list = subtract_course(self.modified_course_list, course["course_code"])
            for course in self.updated_course_list :
                self.modified_course_list = update_course(self.modified_course_list, course)
            self.modified_course_list = sort_by(self.modified_course_list, self.sorting)

        # Lastly, apply filtering.
        for current_filter in self.filtering :
            self.modified_course_list = filter_by(self.modified_course_list, current_filter)

        # Fix the button, so user can filter again.
        self.filter_button.configure(text=self._get_text("Filter Courses"), state="normal")

        # Call update functions -> To take new operations to affect.
        self.___update_program()

    def __update_course(self) -> None:
        """
        Updates course list. It updates the course list by the selected course.
        @Parameters:
            None
        @Returns:
            None
        """
        # Handle no course selection status.
        try :
            selected_course_code = self.display_treeview.item(self.display_treeview.selection())["values"][0]
        except :
            selected_course_code = None

        # Disable update button to prevent multiple update button handle.
        self.update_course_button.configure(text=self._get_text("Updating"), state="disabled")

        # Get course codes
        available_course_codes = []
        for course in self.modified_course_list :
            available_course_codes.append(course["course_code"])

        # Ask user to select course.
        obj = CourseUpdater(self, self.modified_course_list, available_course_codes, self.parsing_language, self.possibleNotations, self.weights, self.possibleCredits, selected_course_code)
        result = obj.get_result()
        if result is not None :
            # Check if user really changed something.
            if result not in self.modified_course_list :
                # Only if course selected, than do operation.
                self.updated_course_list.append(result)
                self.modified_course_list = update_course(self.modified_course_list, result)

        # Fix the button, so user can update again.
        self.update_course_button.configure(text=self._get_text("Update Course"), state="normal")

        # Call update functions -> To take new operations to affect.
        self.___update_program()

    def __add_course(self) -> None:
        """
        Adds course to the course list. It adds the course to the course list by the selected course.
        @Parameters:
            None
        @Returns:
            None
        """
        # Disable add button to prevent multiple add button handle.
        self.add_course_button.configure(text=self._get_text("Adding"), state="disabled")

        # Get course codes
        existing_course_codes = [course["course_code"] for course in self.modified_course_list]

        # Ask user to select course.
        obj = CourseAdder(self, existing_course_codes, self.parsing_language, self.possibleNotations, self.weights, self.possibleCredits)
        result = obj.get_result()
        if result is not None :
            # Only if course selected, than do operation.
            self.added_course_list.append(result)
            self.modified_course_list = add_course(self.modified_course_list, result)

        # Fix the button, so user can add again.
        self.add_course_button.configure(text=self._get_text("Add Course"), state="normal")
        
        # Call update functions -> To take new operations to affect.
        self.___update_program()

    def __remove_course(self) -> None:
        """
        Removes course from the course list. It removes the course from the course list by the selected course.
        @Parameters:
            None
        @Returns:
            None
        """
        # Handle no course selection status.
        try :
            selected_course_code = self.display_treeview.item(self.display_treeview.selection())["values"][0]
        except :
            selected_course_code = None

        # Disable remove button to prevent multiple remove button handle.
        self.remove_course_button.configure(text=self._get_text("Removing"), state="disabled")

        # Get course codes
        existing_course_codes = [course["course_code"] for course in self.modified_course_list]

        # Ask user to select course.
        obj = CourseRemover(self, self.modified_course_list, existing_course_codes, self.parsing_language, selected_course_code)
        result = obj.get_result()
        if result is not None :
            # Only if course selected, than do operation.
            self.subtracted_course_list.append(result)
            # check if this result exists in added course list, then remove from added course list
            self.added_course_list = subtract_course(self.added_course_list, result["course_code"])
            self.modified_course_list = subtract_course(self.modified_course_list, result["course_code"])

        # Fix the button, so user can remove again.
        self.remove_course_button.configure(text=self._get_text("Remove Course"), state="normal")

        # Call update functions -> To take new operations to affect.
        self.___update_program()

    def __sort(self, key : str) :
        """
        Sorts the course list by the given key.
        @Parameters:
            key - Required : Key to sort the course list. (str) -> (course_code, course_name, course_credit, course_grade, course_semester)
        @Returns:
            None
        """
        # Get feature values
        sort_key = key
        should_reverse = self.sorting_reverse_history[sort_key]
        self.sorting_reverse_history[sort_key] = not should_reverse

        # Setup sorting map
        self.sorting = {
            "sort_key" : sort_key,
            "should_reverse" : should_reverse
        }

        # Apply sorting
        self.modified_course_list = sort_by(self.modified_course_list, self.sorting)

        # Call update functions -> To take new operations to affect.
        self.___update_program()