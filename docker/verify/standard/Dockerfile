FROM tomcat:9-alpine

COPY ./gs-rest-service-0.1.0.jar /app/gs-rest-service-0.1.0.jar

WORKDIR /app

ENTRYPOINT ["java", "-jar", "/app/gs-rest-service-0.1.0.jar"]
