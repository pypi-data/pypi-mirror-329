# SCP API
Access information on SCPs through python and javascript! (note: currently being developed, isn't completely released)  
Currently limited from SCP-001 to SCP-5723, Some field may be broken (or just not exist) and may not have properly been copied (I apologize for that, I am constantly working on it.)  

# How it works
We first scrapes (Reason why some field might've not been properly copied) the information off from the [SCP wikidot](https://scp-wiki.wikidot.com/) and stores it in a JSON format.  
We then upload the information up to our site, where the API pulls the data from, inorder to avoid putting load on the [SCP wikidot](https://scp-wiki.wikidot.com/)  

## Process
Create Scraper and get the information (Complete)  
Create the site and upload the files (Being worked upon)  
Create the API (Being worked upon)

### Documentation
  Fields that can be accessed:  
    "URL": URL from where it was scraped  
    "all_text": Complete text from the page  
    "addendums": All addendums on the SCP  
    "documents": All documents on the SCP  
    "notes": Most of the time, it's about licensing stuff and who made it  
    "containment_procedures": Containment Procedures for the SCP  
    "description": Description of the SCP  
    "title": Title of the tab  
    
  Will work on this after the API and site and completed
