import os
import json
import openai
import base64
from openai import OpenAI
from openai import AzureOpenAI
from dotenv import load_dotenv
import tiktoken as TikToken 
load_dotenv()

client = AzureOpenAI( azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
         azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
         api_key=os.getenv("AZURE_OPENAI_KEY"), 
         api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
         
    )


def reason_content(history: dict) -> str:
    # Create a list of messages to send to the OpenAI API
    message = []
    message =[
        {
            "role": "user",
            "content": "You are a geologist, working for an oil company your job is to analyze and summarize data. Do not fabricate facts or change the tone. Respond with the same language of the document page you read. You dont need to create any new ending message for every response like: If you need more assistance feel free to ask. Use the context of the conversation history make a context and reason with the document page image provided in the end.",
        }
     ]
    for h in history:
        message.append(h)
    message.append({
            "role": "user",
            "content": """You should provide a response to try to classify the information provided in geological documents with the following characteristics.
            
1. Geological Survey Reports
	· Description: Comprehensive analyses of the geological characteristics of a specific area.
	· Characteristics:
			o Content: Detailed descriptions of rock types, stratigraphy, structural geology, mineralogy, and tectonic features.
			o Visuals: Geological maps, cross-sections, and 3D models illustrating subsurface structures.
			o Purpose: Identify potential hydrocarbon reservoirs and assess the geological risks associated with drilling.
			o Data Sources: Field observations, sample analyses, and existing geological data.
2. Seismic Interpretation Reports
	· Description: Analyses based on seismic survey data to delineate subsurface features.
	· Characteristics:
			o Content: Interpretation of seismic reflections, fault lines, stratigraphic layers, and potential traps.
			o Visuals: Seismic sections, horizon maps, and 3D seismic volume visualizations.
			o Purpose: Locate oil-bearing formations and plan drilling locations.
			o Tools: Seismic processing software and interpretation platforms.
3. Well Logging Reports
	· Description: Detailed records of geological formations encountered during drilling operations.
	· Characteristics:
			o Content: Measurements from various logging tools (e.g., gamma-ray, resistivity, sonic logs) indicating porosity, permeability, fluid content, and lithology.
			o Visuals: Log curves, lithological columns, and cross-plots.
			o Purpose: Evaluate the potential productivity of a well and inform drilling decisions.
			o Data Integration: Combines real-time drilling data with historical well data.
4. Core Analysis Reports
	· Description: Detailed examinations of core samples extracted from drilled wells.
	· Characteristics:
			o Content: Physical and chemical properties of core samples, including porosity, permeability, mineral composition, and fluid saturation.
			o Visuals: Photographs of core sections, microscopic images, and petrographic analyses.
			o Purpose: Assess reservoir quality and hydrocarbon potential.
			o Laboratory Work: Involves lab testing and analysis of core samples.
5. Reservoir Modeling and Simulation Reports
	· Description: 3D models and dynamic simulations of oil reservoirs.
	· Characteristics:
			o Content: Geological framework, fluid distribution, reservoir properties, and production scenarios.
			o Visuals: 3D reservoir models, simulation animations, and contour maps.
			o Purpose: Predict reservoir behavior, optimize extraction strategies, and enhance recovery rates.
			o Software Tools: Specialized reservoir simulation software (e.g., Petrel, Eclipse).
6. Exploration and Production (E&P) Reports
	· Description: Periodic summaries of exploration activities and production metrics.
	· Characteristics:
			o Content: Exploration successes, drilling results, production data, and operational challenges.
			o Visuals: Graphs showing production trends, maps of exploration areas, and tables summarizing key metrics.
			o Purpose: Inform stakeholders about the progress and performance of exploration and production activities.
			o Frequency: Typically produced quarterly or annually.
7. Environmental Impact Assessments (EIA)
	· Description: Evaluations of the potential environmental effects of oil extraction projects.
	· Characteristics:
			o Content: Analysis of impacts on local ecosystems, water resources, air quality, and socio-economic factors.
			o Visuals: Environmental maps, impact diagrams, and mitigation plans.
			o Purpose: Ensure compliance with environmental regulations and minimize negative impacts.
			o Stakeholders: Regulatory bodies, local communities, and project planners.
8. Feasibility Studies
	· Description: Assessments determining the viability of proposed oil extraction projects.
	· Characteristics:
			o Content: Geological assessments, resource estimates, technical requirements, financial projections, and risk analyses.
			o Visuals: Cost-benefit charts, project timelines, and resource distribution maps.
			o Purpose: Aid decision-making regarding project initiation and investment.
			o Comprehensive Scope: Covers technical, economic, and logistical aspects.
9. Health, Safety, and Environment (HSE) Documentation
	· Description: Guidelines and reports ensuring safe and environmentally responsible operations.
	· Characteristics:
			o Content: Safety protocols, risk assessments, incident reports, and environmental protection measures.
			o Visuals: Safety signages, hazard maps, and compliance checklists.
			o Purpose: Promote workplace safety, prevent accidents, and ensure environmental stewardship.
			o Regulatory Compliance: Aligns with industry standards and legal requirements.
10. Technical Briefs and Presentations
	· Description: Concise documents and slideshows summarizing specific geological findings or methodologies.
	· Characteristics:
			o Content: Key insights, data highlights, and methodological approaches.
			o Visuals: Charts, graphs, schematic diagrams, and bullet-point summaries.
			o Purpose: Communicate technical information to stakeholders, team members, or at conferences.
			o Format: Often used in meetings, seminars, and decision-making forums.
11. Geographic Information System (GIS) Maps
	· Description: Digital maps integrating various geological and geospatial data layers.
	· Characteristics:
			o Content: Terrain features, geological formations, infrastructure locations, and resource distributions.
			o Visuals: Interactive maps with multiple layers, symbols, and legends.
			o Purpose: Support spatial analysis, planning, and visualization of complex geological data.
			o Software Tools: GIS platforms like ArcGIS or QGIS.
12. Regulatory and Compliance Documentation
	· Description: Necessary documents to meet legal and industry standards.
	· Characteristics:
			o Content: Permits, licenses, compliance reports, and audit findings.
			o Visuals: Forms, certification stamps, and compliance matrices.
			o Purpose: Ensure that all exploration and production activities adhere to relevant laws and standards.
			o Mandatory Submissions: Often required by governmental and regulatory bodies.
13. Data Management Reports
	· Description: Documents outlining the organization, storage, and quality control of geological data.
	· Characteristics:
			o Content: Data collection methodologies, storage solutions, data quality assessments, and access protocols.
			o Visuals: Data flowcharts, database schemas, and metadata tables.
			o Purpose: Ensure data integrity, accessibility, and efficient usage across projects.
			o Tools: Database management systems and data visualization tools.
14. Risk Assessment Reports
	· Description: Evaluations identifying and mitigating potential risks associated with oil extraction.
	· Characteristics:
			o Content: Identification of geological, operational, environmental, and economic risks.
			o Visuals: Risk matrices, probability-impact charts, and mitigation strategy diagrams.
			o Purpose: Proactively manage and minimize risks to project success and safety.
			o Methodologies: Often use standardized risk assessment frameworks.

 
Key Characteristics Across Documents:
	· Accuracy and Detail: Precision in data collection, interpretation, and reporting to ensure reliable decision-making.
	· Clarity and Organization: Well-structured with clear headings, sections, and logical flow for easy comprehension.
	· Visual Aids: Use of maps, charts, graphs, and diagrams to illustrate complex information effectively.
	· Technical Rigor: Incorporation of scientific methodologies, standards, and best practices pertinent to geology and oil extraction.
	· Compliance and Standards: Adherence to industry regulations, safety standards, and environmental guidelines.
	· Accessibility: Documents are often shared across multidisciplinary teams, requiring them to be understandable to both technical and non-technical stakeholders.

            
    I want to to read the document presented on the history and provide a response that classifies the information based on the geological data types described above. The response should identify the type of geological data that can be interpreted from the content.""",
        }
    )
    # Add the history to the message if the history is provided
    # print(json.dumps(message))  
    response = client.chat.completions.create(
          model=os.getenv("AZURE_OPENAI_DEPLOYMENT2"),
          messages=message,
     )
    # Send the messages to the OpenAI API
    # Return the response from the OpenAI API
    return response.choices[0].message.content
    #return json.dumps(message)



# Create the main function

def main():
    text_location = "./text"
    document_location = "./document"

   # iterate with every file on the text_location
    for txt_file in [f for f in os.listdir(text_location) if f.endswith(".txt")]:

    # read the content of the txt_file file
        with open(os.path.join(text_location, txt_file), "r") as f:
         history = json.load(f)
        # call the reason_content function
         response = reason_content(history)
         print(response)
         # write the response to a file
        with open("./response.txt", "w") as f:
            f.write(response)
            print("Response saved to response.md")

# call the main function
if __name__ == "__main__":
    main()


