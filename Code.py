import pandas as pd
import numpy as np

def get_region(country):
    """Gets the region of the country introduced as the argument.

    Args:
        country (str): Name of the country.

    Returns:
        (str): Name of the region of the country introduced as an argument.
    """
    
    africa = ["Algeria","Egypt","Ethiopia","Guinea","Liberia","Morocco","Senegal","Togo","Tunisia","Zambia","Angola","Benin","Botswana","Burkina Faso","Burundi","Cameroon",
              "Cabo Verde","Central African Republic","Chad","Comoros","Côte d'Ivoire","Republic of the Congo","Djibouti","Equatorial Guinea","Eritrea","Eswatini","Gabon",
              "Gambia","Ghana","Guinea Bissau","Kenya","Lesotho","Libya","Madagascar","Malawi","Mali","Mauritania","Mauritius","Mozambique","Mayotte","Namibia","Niger","Nigeria",
              "DR Congo","Rwanda","Sao Tome and Principe","Seychelles","Sierra Leone","South Sudan","Sudan","Tanzania","Uganda","Zimbabwe","Ethiopia PDR","Guinea-Bissau", "Congo",
              "Democratic Republic of the Congo","Saint Helena, Ascension and Tristan da Cunha","Somalia","South Africa","Sudan","Western Sahara","Eastern Africa","Middle Africa",
              "Northern Africa","Southern Africa","Western Africa","United Republic of Tanzania","Africa"]
    
    asia = ["China","India","Indonesia","Pakistan","Bangladesh","Japan","Philippines","Viet Nam","Turkey","Iran","Thailand","Myanmar","South Korea","Iraq","Afghanistan","Saudi Arabia",
           "Uzbekistan","Malaysia","Yemen","Nepal","North Korea","Sri Lanka","Kazakhstan","Syria","Cambodia","Jordan","Azerbaijan","United Arab Emirates","Tajikistan","Israel","Laos",
           "Lebanon","Kyrgyzstan","Turkmenistan","Singapore","Oman","State of Palestine","Kuwait","Georgia","Mongolia","Armenia","Qatar","Bahrain","Timor-Leste","Cyprus","Bhutan",
           "Maldives","Brunei","Brunei Darussalam","Democratic People's Republic of Korea","Lao People's Democratic Republic","Palestine","Republic of Korea","Syrian Arab Republic",
           "Asia","Central Asia","Eastern Asia","Southern Asia","South-eastern Asia","Western Asia","China, Hong Kong SAR","China, Macao SAR","China, mainland","China, Taiwan Province of",
           "Russian Federation","Türkiye","Russia"]
    
    america = ["United States of America","Brazil","Mexico","Colombia","Argentina","Canada","Peru","Venezuela","Chile","Ecuador","Guatemala","Bolivia","Haiti","Dominican Republic","Cuba",
               "Honduras","Nicaragua","Paraguay","El Salvador","Costa Rica","Panama","Uruguay","Jamaica","Trinidad and Tobago","Guyana","Suriname","Bahamas","Belize","Barbados",
               "Saint Lucia","Grenada","Saint Vincent and The Grenadines","Antigua and Barbuda","Dominica","Saint Kitts and Nevis","American Samoa", "Anguilla","Aruba","Bermuda",
               "British Virgin Islands","Cayman Islands","Falkland Islands","French Guyana","Greenland","Guadeloupe","Martinique","Montserrat","Netherlands Antilles",
               "Puerto Rico","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Turks and Caicos Islands","United States Virgin Islands","Venezuela","Americas",
               "Northern America","Central America","Caribbean","South America"]
    
    europe = ["Germany","United Kingdom","France","Italy","Spain","Ukraine","Poland","Romania","Netherlands","Belgium", "Belgium-Luxembourg","Czech Republic (Czechia)",
              "Greece","Portugal","Sweden","Hungary","Belarus","Austria","Serbia","Switzerland","Bulgaria","Denmark","Finland","Slovakia","Norway","Ireland","Croatia","Moldova",
              "Bosnia","Bosnia and Herzegovina","Albania","Lithuania","North Macedonia","Slovenia","Latvia","Estonia","Montenegro","Luxembourg","Malta","Iceland","Andorra","Monaco",
              "Liechtenstein","San Marino","Holy See","Channel Islands", "Czechia","Czechoslovakia","Faroe Islands","Gibraltar","Isle of Man","Republic of Moldova","R?nion",
              "Serbia and Montenegro","Svalbard and Jan Mayen Islands","United Kingdom of Great Britain and Northern Ireland","Yugoslav SFR","Europe","Eastern Europe","Northern Europe",
              "Southern Europe","Western Europe","European Union"]
    
    oceania = ["Australia","Cook Islands","Papua New Guinea","New Zealand","Fiji","Solomon Islands","Micronesia","Vanuatu","Samoa","Kiribati","Tonga","Marshall Islands","Palau",
               "Tuvalu","Nauru","French Polynesia","Guam","Kiribati","Micronesia (Federated States of)","New Caledonia","Niue","Norfolk Island","Northern Mariana Islands","Palau",
               "Pitcairn","Pacific Islands Trust Territory","Tokelau","Wallis and Futuna Islands","Oceania","Australia and New Zealand","Melanesia","Polynesia"]

    
    if country in africa:
        return "Africa"
    elif country in asia:
        return "Asia"
    elif country in america:
        return "America"
    elif country in europe:
        return "Europe"
    elif country in oceania:
        return "Oceania"
    else:
        return np.nan

if __name__ == "__main__":

    # CSVs to read
    csv_path = "Total Emissions Per Country (2000-2020).csv"
    csv_path2 = "IND_and_Nep_AQI_Dataset.csv"

    # Clean CSVs    
    df = pd.read_csv(csv_path)
    df["Type_emission"] = df.apply(lambda x: x["Element"].split(" (")[0], axis=1)
    df["Element_split"] = df.apply(lambda x: x["Element"].split(" (")[1].split(")")[0], axis=1)
    df["Original_source"] = df.apply(lambda x: x["Element"].split("from ")[-1].split(" (")[0] if " from " in x["Element"] else x["Element_split"], axis=1)
    
    df["Area"] = df["Area"].apply(lambda x: "Côte d'Ivoire" if x == "C?e d'Ivoire" else x)
    df["Area"] = df["Area"].apply(lambda x: "Türkiye" if x == "T?kiye" else x)
    df["Country"] = df.apply(lambda x: x["Area"].split(" (")[0], axis=1)
    df["Territory"] = df.apply(lambda x: x["Country"].split(", ")[-1], axis=1)
    df["Region"] = df.apply(lambda x: get_region(x["Country"]), axis=1)
    
    
    print(df['Region'].isnull().values.any())
    print(df.isnull().sum().sum())
    res = df.loc[df['Region'].isnull(), 'Country'].drop_duplicates()
    print(res)
    
    df2 = pd.read_csv(csv_path2)
    df2["Date_Hour"] = df2.apply(lambda x: str(x["Day"]) + "-" + str(x["Month"]) + "-" + str(x["Year"]) + " " + str(x["Hour"]), axis=1)
    
    
    # Save CSVs
    df.to_csv("Total_Emissions_Per_Country_(2000-2020)_modified.csv", index=False)
    print("Modified CSV file has been created: Total_Emissions_Per_Country_(2000-2020)_modified.csv")
    
    df2.to_csv("IND_and_Nep_AQI_Dataset_modified.csv", index=False)
    print("Modified CSV file has been created: IND_and_Nep_AQI_Dataset_modified.csv")
