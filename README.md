# Introduction

This repo stores the code for the OneFlorda Linkage Submission System (OLASS)
server application.

The goal of the OLASS server is to achieve de-duplication of the patient
data by generating unique identifiers (UUID) for different combinations of
patient data elements.

For more details about what "linkage" means please see:

* [Design and implementation of a privacy preserving electronic health record linkage tool in Chicago](http://www.ncbi.nlm.nih.gov/pubmed/26104741)
* [A practical approach to achieve private medical record linkage in light of public resources](http://www.ncbi.nlm.nih.gov/pubmed/22847304)

# Authentication

The server implements the "client credentials" grant workflow described in the
[rfc6749](https://tools.ietf.org/html/rfc6749#section-1.3.4).


    +---------+                                  +---------------+
    :         :                                  :               :
    :         :>-- A - Client Authentication --->: Authorization :
    : Client  :                                  :     Server    :
    :         :<-- B ---- Access Token ---------<:               :
    :         :                                  :               :
    +---------+                                  +---------------+


# Developers

For more details on application development please navigate to the
[docs/developers.md](docs/developers.md).


# License

This project is covered by the [MIT License](LICENSE).

# Contributors

The application was designed and implemented by Andrei Sura with tremendous
support, fedback and contributions from the
[BMI team](https://github.com/orgs/ufbmi/people).

For the complete list of contributors please see [AUTHORS.md](AUTHORS.md)
