FROM python:3.9.7

WORKDIR /home/netwatch

COPY entrypoint.sh /home/netwatch/entrypoint.sh
COPY nginx.conf /etc/nginx/customnginx.conf
COPY backend/ /home/netwatch/backend/
COPY client/dist/ /home/netwatch/client/

RUN pip3 install -r ./backend/requirements.txt 
RUN chmod +x entrypoint.sh
RUN apt update --yes
RUN apt install nginx --yes

#Expose client port
EXPOSE 8080 

#Expose API port
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]