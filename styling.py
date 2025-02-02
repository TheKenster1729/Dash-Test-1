import pandas as pd
from plotly.colors import n_colors, hex_to_rgb, convert_dict_colors_to_same_type
from PIL import ImageColor
import json

class Color:
    def __init__(self):
        self.palette = {
            "Red 100": "2d0709",
            "Red 90": "520408",
            "Red 80": "750e13",
            "Red 70": "a2191f",
            "Red 60": "da1e28",
            "Red 50": "fa4d56",
            "Red 40": "ff8389",
            "Red 30": "ffb3b8",
            "Red 20": "ffd7d9",
            "Red 10": "fff1f1",
            "Magenta 100": "2a0a18",
            "Magenta 90": "510224",
            "Magenta 80": "740937",
            "Magenta 70": "9f1853",
            "Magenta 60": "d02670",
            "Magenta 50": "ee5396",
            "Magenta 40": "ff7eb6",
            "Magenta 30": "ffafd2",
            "Magenta 20": "ffdee8",
            "Magenta 10": "fff0f7",
            "Purple 100": "1c0f30",
            "Purple 90": "31135e",
            "Purple 80": "491d8b",
            "Purple 70": "6929c4",
            "Purple 60": "8a3ffc",
            "Purple 50": "a56eff",
            "Purple 40": "be95ff",
            "Purple 30": "d4bbff",
            "Purple 20": "e8daff",
            "Purple 10": "f6f2ff",
            "Blue 100": "001141",
            "Blue 90": "001d6c",
            "Blue 80": "002d9c",
            "Blue 70": "0043ce",
            "Blue 60": "0f62fe",
            "Blue 50": "4589ff",
            "Blue 40": "78a9ff",
            "Blue 30": "a6c8ff",
            "Blue 20": "d0e2ff",
            "Blue 10": "edf5ff",
            "Cyan 100": "061727",
            "Cyan 90": "012749",
            "Cyan 80": "003a6d",
            "Cyan 70": "00539a",
            "Cyan 60": "0072c3",
            "Cyan 50": "1192e8",
            "Cyan 40": "33b1ff",
            "Cyan 30": "82cfff",
            "Cyan 20": "bae6ff",
            "Cyan 10": "e5f6ff",
            "Teal 100": "081a1c",
            "Teal 90": "022b30",
            "Teal 80": "004144",
            "Teal 70": "005d5d",
            "Teal 60": "007d79",
            "Teal 50": "009d9a",
            "Teal 40": "08bdda",
            "Teal 30": "3ddbd9",
            "Teal 20": "9ef0f0",
            "Teal 10": "d9f9fb",
            "Green 100": "071908",
            "Green 90": "022d0d",
            "Green 80": "044317",
            "Green 70": "0e6027",
            "Green 60": "198038",
            "Green 50": "24a148",
            "Green 40": "42be65",
            "Green 30": "6fdc8c",
            "Green 20": "a7f0ba",
            "Green 10": "defbec",
            "Cool Gray 100": "121619",
            "Cool Gray 90": "21272a",
            "Cool Gray 80": "343a3f",
            "Cool Gray 70": "4d5358",
            "Cool Gray 60": "697077",
            "Cool Gray 50": "878d96",
            "Cool Gray 40": "a2a9b0",
            "Cool Gray 30": "c1c7cd",
            "Cool Gray 20": "dde1e6",
            "Cool Gray 10": "f2f4f8",
            "Gray 100": "161616",
            "Gray 90": "262626",
            "Gray 80": "393939",
            "Gray 70": "525252",
            "Gray 60": "6f6f6f",
            "Gray 50": "8d8d8d",
            "Gray 40": "a8a8a8",
            "Gray 30": "c6c6c6",
            "Gray 20": "e0e0e0",
            "Gray 10": "f4f4f4",
            "Warm Gray 100": "171414",
            "Warm Gray 90": "272525",
            "Warm Gray 80": "3c3838",
            "Warm Gray 70": "565151",
            "Warm Gray 60": "726e6e",
            "Warm Gray 50": "8f8b8b",
            "Warm Gray 40": "ada8a8",
            "Warm Gray 30": "cac5c4",
            "Warm Gray 20": "e5e0df",
            "Warm Gray 10": "f7f3f2"
            }
        self.hex_palette = {key: '#' + value for key, value in self.palette.items()}
        # self.region_colors = {"GLB": "rgb(127, 127, 127)", "USA": "rgb(0, 83, 154)", "CAN": "rgb(162, 25, 31)", "MEX": "rgb(4, 67, 23)", "JPN": "rgb(250, 77, 86)",
        #                       "ANZ": "rgb(0, 67, 206)", "EUR": "rgb(255, 221, 0)", "ROE": "rgb(61, 219, 217)", "RUS": "rgb(1, 39, 73)", "ASI": "rgb(73, 29, 139)",
        #                       "CHN": "rgb(82, 4, 8)", "IND": "rgb(245, 222, 179)", "BRA": "rgb(111, 220, 140)", "AFR": "rgb(166, 200, 255)", "MES": "rgb(212, 187, 255)",
        #                       "LAM": "rgb(0, 65, 68)", "REA": "rgb(130, 207, 255)", "KOR": "rgb(0, 93, 93)", "IDZ": "rgb(114, 110, 110)"}
        self.region_colors = {"GLB": "#491d8b", "USA": "#5492C5", "CAN": "#1D4971", "MEX": "#80CDDF", "JPN": "#6E37A3",
                              "ANZ": "#1B344A", "EUR": "#679C82", "ROE": "#91C96E", "RUS": "#2B4739", "ASI": "#493B82",
                              "CHN": "#725D7A", "IND": "#979576", "BRA": "#16824D", "AFR": "#1A5A2D", "MES": "#D6D092",
                              "LAM": "#38A8A3", "REA": "#CCBE2C", "KOR": "#52CE02", "IDZ": "#B03AC2"}
        self.scenario_colors = {"15C_med": "#750e13", "15C_opt": "#ffb3b8", "About15C_pes": "#740937", "About15C_med": "#ffafd2",
                                "About15C_opt": "#491d8b", "2C_pes": "#d4bbff", "2C_med": "#002d9c", "2C_opt": "#a6c8ff",
                                "Above2C_pes": "#003a6d", "Above2C_med": "#82cfff", "Above2C_opt": "#004144", "Ref": "#3ddbd9"}
        self.scenario_markers = {"Ref": "solid", "Above2C_med": "dot", "2C_med": "dash"}
        self.histogram_patterns = {"Ref": "", "2C": "/"}
        self.parallel_coords_colors = ["#785EF0", "#FFB000"]

    def generate_palette(self, n):
        rgb_colors = convert_dict_colors_to_same_type(self.hex_palette)
        return n_colors(rgb_colors["Red 80"], rgb_colors["Cool Gray 50"], n, colortype = "rgb")

    def convert_to_fill(self, color, alpha = 0.3):
        # add alpha channel
        rgb = ImageColor.getcolor(color, "RGB")
        rgba = tuple(list(rgb) + [alpha])
        return "rgba" + str(rgba)

    def lighten_hex(self, hex_color, brightness_offset = 1):
        if len(hex_color) != 7:
            raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
        rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
        new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
        new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
        # hex() produces "0x88", we want just "88"
        return "#" + "".join([hex(i)[2:] for i in new_rgb_int])

    def get_color_for_timeseries(self, styling_option, param):
        if styling_option == "by-region":
            color = self.region_colors[param]
        elif styling_option == "by-scenario":
            color = self.scenario_colors[param]
        elif styling_option == "standard":
            base_shade = self.region_colors[param[0]]
            amount_to_lighten = Options().scenarios.index(param[1])
            color = self.lighten_hex(base_shade, brightness_offset = amount_to_lighten*8)

        return color

class Readability:
    def __init__(self):
        self.naming_df = pd.read_csv(r"display_names.csv")
        self.naming_dict_long_names_first = {i["Full Output Name"]:i["Display Name"] for i in self.naming_df.to_dict("records")}
        self.naming_dict_display_names_first = {v:k for k, v in self.naming_dict_long_names_first.items()}

    def ordinal(self, n):
        """
        Returns the ordinal number string of an integer, n
        e.g. 1 -> '1st', 2 -> '2nd', 3 -> '3rd', 11 -> '11th'
        """
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

class Options:
    def __init__(self):
        self.region_names = ["GLB", "USA", "CAN", "MEX", "JPN", "ANZ", "EUR", "ROE", "RUS", "ASI", "CHN", "IND",
                                "BRA", "AFR", "MES", "LAM", "REA", "KOR", "IDZ"]
        self.scenarios = ['15C_med', '15C_opt', 'About15C_pes', 'About15C_med', 'About15C_opt','2C_pes', '2C_med', '2C_opt', 'Above2C_pes', 'Above2C_med', 'Above2C_opt', 'Ref']
        self.scenario_display_names = {"15C_med": "1.5C Med", "15C_opt": "1.5C Opt", "2C_med": "2C Med", "2C_opt": "2C Opt", "2C_pes": "2C Pes", "About15C_opt": "About 1.5C Opt", "About15C_med": "About 1.5C Med",
                                       "About15C_pes": "About 1.5C Pes", "Above2C_med": "Above 2C Med", "Above2C_opt": "Above 2C Opt", "Above2C_pes": "Above 2C Pes", "Ref": "Ref"}
        self.scenario_display_names_rev = {v:k for k, v in self.scenario_display_names.items()}
        self.outputs = Readability().naming_dict_long_names_first.keys()
        self.years = [i for i in range(2020, 2101, 5)]
        self.markers = {"Ref": "circle", "2C": "triangle-up-open-dot"}
        self.input_names = [
                    "E-LK",
                    "E-NE(final)",
                    "E-NOE",
                    "ESUBE(EL/EI)",
                    "ESUBE(oth)",
                    "LK AGRI",
                    "LK ENOE",
                    "LK ELEC",
                    "LK EINT",
                    "LK SERV",
                    "LK OTHR",
                    "LK TRANS",
                    "LK DWE",
                    "LK FOOD",
                    "FF-COAL",
                    "FF-OIL",
                    "FF-GAS",
                    "VINT",
                    "AEEI USA",
                    "AEEI CAN",
                    "AEEI MEX",
                    "AEEI JPN",
                    "AEEI ANZ",
                    "AEEI EUR",
                    "AEEI ROE",
                    "AEEI RUS",
                    "AEEI ASI",
                    "AEEI KOR",
                    "AEEI IDZ",
                    "AEEI CHN",
                    "AEEI IND",
                    "AEEI BRA",
                    "AEEI AFR",
                    "AEEI MES",
                    "AEEI LAM",
                    "AEEI REA",
                    "oil",
                    "gas",
                    "coal",
                    "NGCC",
                    "PC",
                    "Nuclear",
                    "PV",
                    "wind",
                    "Bio",
                    "NGCAP",
                    "PCCAP",
                    "BioCCS",
                    "WindGas",
                    "WindBio",
                    "Biol-Oil",
                    "TFP",
                    "Pop",
                    "USA TFP",
                    "Non-USA TFP",
                    "USA Pop",
                    "Non-USA Pop",
                    "CHN TFP",
                    "Non-CHN TFP",
                    "CHN Pop",
                    "Non-CHN Pop",
                    "EUR TFP",
                    "Non-EUR TFP",
                    "EUR Pop",
                    "Non-EUR Pop",
                    "CAN TFP",
                    "Non-CAN TFP",
                    "CAN Pop",
                    "Non-CAN Pop",
                    "MEX TFP",
                    "Non-MEX TFP",
                    "MEX Pop",
                    "Non-MEX Pop",
                    "JPN TFP",
                    "Non-JPN TFP",
                    "JPN Pop",
                    "Non-JPN Pop",
                    "ANZ TFP",
                    "Non-ANZ TFP",
                    "ANZ Pop",
                    "Non-ANZ Pop",
                    "ROE TFP",
                    "Non-ROE TFP",
                    "ROE Pop",
                    "Non-ROE Pop",
                    "RUS TFP",
                    "Non-RUS TFP",
                    "RUS Pop",
                    "Non-RUS Pop",
                    "ASI TFP",
                    "Non-ASI TFP",
                    "ASI Pop",
                    "Non-ASI Pop",
                    "IND TFP",
                    "Non-IND TFP",
                    "IND Pop",
                    "Non-IND Pop",
                    "BRA TFP",
                    "Non-BRA TFP",
                    "BRA Pop",
                    "Non-BRA Pop",
                    "AFR TFP",
                    "Non-AFR TFP",
                    "AFR Pop",
                    "Non-AFR Pop",
                    "MES TFP",
                    "Non-MES TFP",
                    "MES Pop",
                    "Non-MES Pop",
                    "LAM TFP",
                    "Non-LAM TFP",
                    "LAM Pop",
                    "Non-LAM Pop",
                    "REA TFP",
                    "Non-REA TFP",
                    "REA Pop",
                    "Non-REA Pop",
                    "KOR TFP",
                    "Non-KOR TFP",
                    "KOR Pop",
                    "Non-KOR Pop",
                    "IDZ TFP",
                    "Non-IDZ TFP",
                    "IDZ Pop",
                    "Non-IDZ Pop"
                ]
        # in case
        # name = str(bound) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= bound % 100 < 20 else bound % 10, "th")

class FinishedFigure(Color, Readability, Options):
    def __init__(self, fig_object):
        Color.__init__(self)
        Readability.__init__(self)
        Options.__init__(self)
        self.figure_object = fig_object
        self.display_names_for_figure_type = {"output-timeseries": "Time Series for ", "input-output-mapping-main": "CART Results for ",
                                              "choropleth-map": "Choropleth Map for ", "ts-clustering": "Time Series Clusters for ",
                                              "output-output-mapping-main": "Output-Output Mapping for ", "regional-heatmaps": "Regional Heatmap for ",
                                              "permutation-importance": "Permutation Importance for ", "ts-clustering-cart": "Time Series Clusters CART for "}
        
    def split_label(self, label, max_line_length):
        words = label.split()
        lines = []
        current_line = []

        for word in words:
            # Check if adding the next word exceeds the max line length
            if sum(len(w) for w in current_line) + len(word) + len(current_line) - 1 < max_line_length:
                current_line.append(word)
            else:
                # Join current line and start a new line
                lines.append(' '.join(current_line))
                current_line = [word]

        # Append the last line
        if current_line:
            lines.append(' '.join(current_line))

        return '<br>'.join(lines)

    def style_figure(self):
        # this logic block handles the output display name portion of titling figures
        if self.figure_object.output in self.outputs:
            output_name_for_title = self.naming_dict_long_names_first[self.figure_object.output]
        else:
            # assume this covers all cases, as an output not present in the data set originally
            # nor present as a custom output should not occur
            
            output_name_for_title = json.loads(self.figure_object.output)["name"]

        # define overall title
        if self.figure_object.year:
            title = self.display_names_for_figure_type[self.figure_object.figure_type] + output_name_for_title + ", " + self.figure_object.region + " " + self.scenario_display_names[self.figure_object.scenario] + " " + str(self.figure_object.year)
        else:
            title = self.display_names_for_figure_type[self.figure_object.figure_type] + output_name_for_title + ", " + self.figure_object.region + " " + self.scenario_display_names[self.figure_object.scenario]
        self.figure_object.fig.update_layout(title_text = title,
                                      margin = dict(l = 20, r = 20),
                                      title = title,
                                      height = 600)
        # plot-specific changes
        if self.figure_object.figure_type == "input-output-mapping-main" or self.figure_object.figure_type == "output-output-mapping-main" or self.figure_object.figure_type == "ts-clustering-cart":
            self.figure_object.fig.update_yaxes(title_text = "Feature Importance", row = 1, col = 1)
            self.figure_object.fig.update_annotations(yshift = 20)
            
            def new_name_for_bar_graph(current_name):
                if current_name in self.outputs:
                    new_name = self.split_label(self.naming_dict_long_names_first[current_name], 12)
                else:
                    new_name = self.split_label(current_name, 12)

                return new_name
            self.figure_object.fig.data[0]["x"] = [new_name_for_bar_graph(name) for name in self.figure_object.fig.data[0]["x"]]

            for dimension in self.figure_object.fig.data[1]["dimensions"]:
                current_name = dimension.label
                if current_name in self.outputs:
                    new_name = self.split_label(self.naming_dict_long_names_first[current_name], 12)
                else:
                    new_name = self.split_label(current_name, 12)
                dimension.label = new_name
            
            self.figure_object.fig.data[1].labelangle = 30
            self.figure_object.fig.update_layout(margin=dict(b=100))

        if self.figure_object.figure_type == "choropleth-map":
            self.figure_object.fig.update_layout(
                            geo = dict(showframe = False,
                                showcoastlines = False,
                                projection_type = 'equirectangular'
                            ),
                            height = 600,
                            width = 1200
                        )
        if self.figure_object.figure_type == "ts-clustering":
            self.figure_object.fig.update_layout(
                yaxis = dict(title = dict(text = output_name_for_title, font = dict(size = 16))),
                xaxis = dict(title = dict(text = "Year", font = dict(size = 16)))
            )

        if self.figure_object.figure_type == "permutation-importance":
            self.figure_object.fig.update_layout(
                yaxis = dict(title = dict(text = "Importance", font = dict(size = 16))),
                xaxis = dict(title = dict(text = "Feature", font = dict(size = 16)))
            )
        if self.figure_object.figure_type == "output-output-mapping-main":
            def new_name_for_bar_graph(current_name):
                if current_name in self.outputs:
                    new_name = self.split_label(self.naming_dict_long_names_first[current_name], 12)
                else:
                    new_name = self.split_label(current_name, 12)

                return new_name
            self.figure_object.fig.data[0]["x"] = [new_name_for_bar_graph(name) for name in self.figure_object.fig.data[0]["x"]]

            for dimension in self.figure_object.fig.data[1]["dimensions"]:
                current_name = dimension.label
                if current_name in self.outputs:
                    new_name = self.split_label(self.naming_dict_long_names_first[current_name], 12)
                else:
                    new_name = self.split_label(current_name, 12)
                dimension.label = new_name

            self.figure_object.fig.data[1].labelangle = 30

        if self.figure_object.figure_type == "regional-heatmap":
            self.figure_object.fig.update_layout(
                height = 600,
                width = 1200
            )

    def make_finished_figure(self):
        self.style_figure()
        return self.figure_object.fig

if __name__ == "__main__":
    region_colors = {"GLB": "#7F7F7F", "USA": "#5492C5", "CAN": "#1D4971", "MEX": "#80CDDF", "JPN": "#6E37A3",
                            "ANZ": "#1B344A", "EUR": "#679C82", "ROE": "#91C96E", "RUS": "#2B4739", "ASI": "#493B82",
                            "CHN": "#725D7A", "IND": "#979576", "BRA": "#16824D", "AFR": "#1A5A2D", "MES": "#D6D092",
                            "LAM": "#38A8A3", "REA": "#CCBE2C", "KOR": "#52CE02", "IDZ": "#B03AC2"}

    from figure import OutputOutputMappingPlot
    from sql_utils import SQLConnection, DataRetrieval

    db_obj = SQLConnection("all_data_jan_2024")
    df = DataRetrieval(db_obj, "consumption_billion_USD2007", "GLB", "Ref", 2050).mapping_df()
    fig = OutputOutputMappingPlot("consumption_billion_USD2007", "GLB", "Ref", 2050, df, db_obj)
    finished_fig = FinishedFigure(fig).make_finished_figure()
    finished_fig.show()