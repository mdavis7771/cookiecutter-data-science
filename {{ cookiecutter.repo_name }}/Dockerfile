FROM conda/miniconda2:latest
ENTRYPOINT ["/bin/bash", "-c"]
EXPOSE 5000
COPY environment.yml /app/

RUN conda env create -f /app/environment.yml -n {{ cookiecutter.repo_name }}

COPY . /app

WORKDIR /app

ENTRYPOINT [ "/bin/bash", "-c", "source activate {{ cookiecutter.repo_name }} && python api.py" ]
