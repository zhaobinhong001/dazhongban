FROM java:alpine

COPY ./docker/verify/gs-rest-service-0.1.0.jar /app/gs-rest-service-0.1.0.jar

WORKDIR /app

ENTRYPOINT ["java", "-jar", "/app/gs-rest-service-0.1.0.jar"]
