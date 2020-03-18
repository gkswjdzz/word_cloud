FROM rackspacedot/python37:latest

CMD ["bash"]

RUN mkdir workspace
WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
ENTRYPOINT ["python", "server.py"]