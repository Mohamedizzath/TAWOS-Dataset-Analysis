## Analysis of TAWOS dataset

### Python virtual environment setup

Inside terminal run following command to setup juypter notebooks

```
cd TAWOS-Dataset-Analysis
python -m venv ./env
.\env\Scripts\activate

pip install jupyter
pip install ipython
pip install ipykernel

ipython kernel install --user --name=env
python -m ipykernel install --user --name=myenv
```

Modify connection configurations in notebooks cells
