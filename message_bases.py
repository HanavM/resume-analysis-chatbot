message_base_for_processing = [
    {"role": "system", "content": """
    You are going to be extracting structured data from sample resumes texts that I give you. I need all the extracted structure data to be in this format:
    sampleJsonStructure = {
        "name": None,
        "summary": None,
        "education": [
            {
                "institution": None,
                "field": None,
                "education_level": None,
                "subject_area": None,
                "start_year": None,
                "end_year": None
            }
        ],
        "experience": [
            {
                "title": None,
                "employer": None,
                "skills_experiences": [
                    {"area": None, "skill": None}
                ],
                "start_year": None,
                "end_year": None,
                "contributions": [
                    {"area": None, "contribution": None}
                ]
            }
        ],
        "skills": [
            {
                "area": None,
                "skill": None
            }
        ],
        "certifications": [
            {
                "area": None,
                "provider": None,
                "name": None,
                "year": None
            }
        ],
        "platforms": [
            {
                "area": None,
                "name": None
            }
        ],
        "interests": [
            {
                "area": None,
                "name": None
            }
        ],
        "contact_info": {
            "email": None,
            "phone": None,
            "address": None
        },
        "projects": [
            {
                "name": None,
                "area": None,
                "description": None,
                "start_year": None,
                "end_year": None,
                "technologies": [None]
            }
        ],
        "languages": [
            {
                "language": None,
                "proficiency": None
            }
        ]
    }

    The format is a python dictionary and some keys are lists of dictionaries. Leave any field that is not found in the text as None. It has to be None (like in python), not null! You can infer certain fields like 'area' which is the subject field of a certain entity.
    But for the rest, you should just be cutting and pasting text from the resumes.

    Convert this resume text into the structured data in the rules I told you, the structure I told you, and like the example I showed.
    Make sure to use python syntax! Do not use the "null" keyword; use "None". Make sure all dictionaries and lists are in proper syntax.
    When you return text, only output the dictionary starting from the braces. Do not tell me anything else or give me the name of the json sturcture variable too. Do this so that I can easily convert it into a json!

    """
    },
    {"role": "system", "content": """
    Here is an example. This is the resume, unstructured text:
        Jordan Reese Patterson
    Software Developer
    (469) 647-6531
    Richardson, TX
    jordanreesepatterson@gmail.com
    Career Summary
    Expertise in web applications, custom software development, and systems administration. Most
    recent work includes development with React and NET N-tier architecture web applications.
    Background influenced by managing Unix based systems. Adaptable to any form of IT work, and
    capable of both working as part of a team, or independently. Currently improving architectural
    understanding and system design.
    Achievements Summary

    ApplyNow (Primelending): Manage a small team in the rebuilding of the application, migrating
    from antiquated AngularJS to a modern framework, ReactJS + NextJS. Improve performance,
    reduce errors logged, and improve UX on the platform.

    CarOffer: Industry's first (and only) instant trade platform geared to solve what is known as the
    “Aged Inventory Problem”. Product streamlines selling of inventory units for consumers and takes
    them back into profitability. Transaction based system which has generated over $1,000,000 in
    revenue within 3 months of going live.
    Technical Summary
    JavaScript/TypeScript
    ReactJS (redux, dva, antd)
    JIRA/git
    C# (.NET core)
    Front End Development
    SQL
    Software Development Career History
    Pearl Solutions(Aug 2016 - June 2020, July 2021 - current) | Software Developer

    Rebuilt flagship product from ground up (with team) using latest technologies in React and Redux

    Front-end & API layer work for multiple N-tier .NET applications

    Create and own user interfaces of new and existing web reports, integrate third party APIs for
    cooperation with services

    Create and maintain back end API services
    PrimeLending (June 2020 - July 2021) | Senior Software Developer

    Maintain and upgrade site as needed, troubleshoot breakdowns and perform preventative
    maintenance. Identify and evaluate improvement options; introducing new technology options for
    enhanced functionality and visibility.

    Responsible for rebuilding the application using ReactJS from AngularJS.
    TynetUSA (Jan 2015- Aug 2016) | Software Developer

    Maintained strict medical and billing standards required by Medicare and HMOs around the
    country. Built large forms securely handling large amounts of medical and personal information
    into SQL Server or exported PDF/CSV.


    And this was the structured data:
    {
      "name": "Jordan Reese Patterson",
      "summary": "Expertise in web applications, custom software development, and systems administration. Most recent work includes development with React and NET N-tier architecture web applications. Background influenced by managing Unix based systems. Adaptable to any form of IT work, and capable of both working as part of a team, or independently. Currently improving architectural understanding and system design.",
      "education": [
          null
      ],
      "experience": [
          {
              "title": "Software Developer",
              "employer": "Pearl Solutions",
              "skills_experiences": [
                  {
                      "area": "Software",
                      "skill": "Front End Development"
                  },
                  {
                      "area": "Software",
                      "skill": ".NET"
                  }
              ],
              "start_year": "2016",
              "end_year": "Present",
              "contributions": [
                  {
                      "area": "product development",
                      "contribution": "Rebuilt flagship product from ground up (with team) using latest technologies in React and Redux"
                  },
                  {
                      "area": "Software",
                      "contribution": "Front-end & API layer work for multiple N-tier .NET applications"
                  },
                  {
                      "area": "product development",
                      "contribution": "Create and own user interfaces of new and existing web reports, integrate third party APIs for cooperation with services"
                  },
                  {
                      "area": "product development",
                      "contribution": "Create and maintain back end API services"
                  },
                  {
                      "area": "project",
                      "contribution": "Led the development of CarOffer, an industry-first instant trade platform generating over $1,000,000 in revenue within 3 months of going live"
                  },
                  {
                      "area": "project",
                      "contribution": "Managed a small team in rebuilding ApplyNow, migrating the application from AngularJS to ReactJS + NextJS, improving performance, and reducing errors"
                  }
              ]
          },
          {
              "title": "Senior Software Developer",
              "employer": "PrimeLending",
              "skills_experiences": [
                  {
                      "area": "Software",
                      "skill": "ReactJS"
                  },
                  {
                      "area": "Software",
                      "skill": "Site Maintenance"
                  }
              ],
              "start_year": "2020",
              "end_year": "2021",
              "contributions": [
                  {
                      "area": "software upgrade",
                      "contribution": "Rebuilt the application using ReactJS from AngularJS"
                  },
                  {
                      "area": "site management",
                      "contribution": "Maintained and upgraded the site, identified improvement options, and introduced new technology"
                  }
              ]
          },
          {
              "title": "Software Developer",
              "employer": "TynetUSA",
              "skills_experiences": [
                  {
                      "area": "Medical Software",
                      "skill": "Billing Standards"
                  },
                  {
                      "area": "Database",
                      "skill": "SQL Server"
                  }
              ],
              "start_year": "2015",
              "end_year": "2016",
              "contributions": [
                  {
                      "area": "form handling",
                      "contribution": "Built large forms to securely handle medical and personal information into SQL Server or export to PDF/CSV"
                  }
              ]
          }
      ],
      "skills": [
          {
              "area": "coding",
              "skill": "JavaScript/TypeScript"
          },
          {
              "area": "coding",
              "skill": "ReactJS (redux, dva, antd)"
          },
          {
              "area": "Software",
              "skill": "JIRA/git"
          },
          {
              "area": "Software",
              "skill": "C# (.NET core)"
          },
          {
              "area": "Software",
              "skill": "Front End Development"
          },
          {
              "area": "Database",
              "skill": "SQL"
          }
      ],
      "certifications": [
          null
      ],
      "platforms": [
          {
              "area": "Software",
              "name": ".NET"
          }
      ],
      "interests": [
          null
      ],
      "contact_info": {
          "email": "jordanreesepatterson@gmail.com",
          "phone": "(469) 647-6531",
          "address": "Richardson, TX"
      },
      "projects": [
          null
      ],
      "languages": [
          null
      ]
    }

    In the next message is the text of the resume you will get the output of.
    Convert this resume text into the structured data in the rules I told you, the structure I told you, and like the example I showed.
    Do not put multiple distinct fields into one field. For example a list of skills should not be put as one string of all skills into the field.
    Make sure to use python syntax! Do not use the "null" keyword; use "None". Make sure all dictionaries and lists are in proper syntax.
    When you return text, only output the dictionary starting from the braces. Do not tell me anything else or give me the name of the json sturcture variable too. Do this so that I can easily convert it into a json!

    """}
]


message_base_for_prompt = [
    {"role": "Structured text extractor.", "content": """
      You need to take user-entered queries on applicant resumes and extract what the query is looking for in these categories: name, education, experience, skills, certifications, platforms, interests, projects, and languages.
      Your extracted data has to be a python dictionary but without the variable name and declaration. You just need to return the dictionary in braces, essentially a JSON. Each category listed is a key of the dictionary.
      If there is no information in the query related to a certain category, put None as the value for that key. Make sure you spell everything in the exact same way as listed in the categories that I gave you.
      Ensure that everything fits python syntax so please use None instead of NaN or null. Also, each key is a list of possible values. If there is multiple values for one key, make a list and put each value in the list seperately.
      It should not be one long string with all of values. It should be a list with each value as a seperate item in the string. Even if there is only one value, put a list and have there only be one string in that list.
      An example query: Hey! Show me all the applicants who got a Master's Degree in a computer-related degree, are great at marketing and sales, know how to use Microsoft 365 and G-Suite, and can speak English and French.
      Example structure:
      {
        "name": None,
        "education": "Master's Degree in a computer degree",
        "experience": None,
        "skills": ["marketing", "sales"],
        "certifications": None,
        "platforms": ["Microsoft 365", "G-Suite"],
        "interests": None,
        "projects": None,
        "languages": ["English", "French"],
      }
      Notice how in this example, each value is either a list of values or is None. Make sure that if something is not present in the query, leave it as None.
      Also make sure you spell every category properly and put them in the right order. No key should be missing.

      An example query: Applicants who have worked as a consultant and a software engineer. They need to have an AWS certification. They also need to have past AI medical imaging projects. Make sure they are good at public speaking.
      Example structure:
      {
        "name": None,
        "education": None,
        "experience": ["consultant", "software engineer"],
        "skills": ["public speaking"],
        "certifications": "AWS Certification",
        "platforms": None,
        "interests": None,
        "projects": None,
        "languages": None,
      }
      Notice how even though there is only skill in this example, it is still held in a list. Make sure you do this.

      In the next message is the query that I need you to segment in the same way. Please return me the output as a python dictionary but do not have it as a variable declaration. Just do it in the way I gave examples of.
      Again, make sure that each field of the output dictionary is either None or a list of values, even if it is a list of one value.
    """}
]


generation_base_0 = [
    {"role": "generator in a RAG pipeline", "content": """
      You are a RAG pipeline for numerous resumes. In the next message you will recieve the prompt that was given. From that prompt, I have extracted all the resumes that satisfy that prompt.
    """},
]

generation_base_1 = [
    {"role": "generator in a RAG pipeline", "content": """
      Answer the prompt by saying that these resumes satisfy the prompt.
      So if the prompt asks to see all resumes of people who have skills in python, explicitly say something like: "here are the resumes of people with skills in python. blah blah blah"
      Then, give a brief summary (2-3 sentences) of the resumes. Also highlight the names of a couple (about 1-3) candidates that are the most exceptional. Don't create any new candidates.
      If there are only 2 candidates, only highlight those 2.
      You do not need to return all the resumes. Just the smmary and the names of those highlights.
      You need to make this a friendly conversational message so answer in a proper format. In the next message you will receive all the resumes.
    """}
]
