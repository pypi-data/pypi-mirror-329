from setuptools import setup 

setup(
    name = "rskpp",
    version = "0.1", 
    description= "Rejection Sampling Approach to k-means++ seeding",
    packages=["rskpp"], 
    author="Poojan Shah", 
    author_email="cs1221594@iitd.ac.in", 
    zip_safe = False, 
    install_requires=[
        "numpy",
    ],
)