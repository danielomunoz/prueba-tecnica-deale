# Prueba técnica para el puesto de desarrollador backend - Deale - Daniel Muñoz Amaya

## Detalle de los pasos seguidos para el desarrollo
* Paso 1: Creación de una cuenta gratuita en AWS (link: https://aws.amazon.com/es/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all)
* Paso 2: Creación de una cuenta en serverless (link: https://app.serverless.com/?view=register)
* Paso 3: Creación de una app de Serverless framework en el directorio de nuestro repositorio. Resultado: /deale-app folder.
    * ```cd ~/Prueba\ técnica\ -\ Deale```
    * ```npm i -g serverless```
    * ```serverless --org=danielomunoz --app=deale-app --name=deale-app --template=aws-python-http-api```
    * Seleccionamos como método de autenticación con AWS: AWS Access role
    * Añadimos un provider desde el panel de la web de Serverless. En este caso: AWS.
    * Le colocamos de nombre "deale-user" al access-role, y creamos en AWS un access key, con su ID y su clave -> Colocamos ambos en el modal de Serverless para crear el provider -> Pulsamos crear provider.
    * El cli nos indica que el provider ha sido creado satisfactoriamente -> Pulsamos "n" cuando nos pregunta si queremos desplegar ya nuestra lambda, puesto que aún no hemos codificado su lógica.
* Paso 4: Definición de los dos métodos a utilizar para la tabla FavouriteOrganizationTable de base de datos en el fichero serverless.yml: getAllFavouritesOrganizations y postFavouriteOrganization
* Paso 5: Añado como zona del provider eu-west-1 en el fichero serverless.yml. Ésto no es necesario pero me gusta seleccionar Europa (Irlanda) como zona para asegurar que el despliegue y los servicios se ejecutan con velocidad.
* Paso 6: Añado la tabla de DynamoDB en el fichero serverless.yml (apartado "resources").
* Paso 7: Desplegamos el serverless.yml para comprobar que la tabla de DynamoDB se ha creado correctamente. ```serverless deploy```
* Paso 8: Copiamos el ARN de la nueva tabla creada y la pegamos en el fichero serverless.yml dentro del apartado "provider", para indicar al proyecto que tenemos permiso para utilizarla.
* Paso 9: Desplegamos el proyecto de nuevo para actualizar nuestros permisos sobre la tabla de DynamoDB.
* Paso 10: Añadimos lógica para el handler y actualizamos las funciones referentes a las lambdas que van a ser creadas en el fichero serverless.yml.
* Paso 11: Desplegamos de nuevo la API y testeamos su funcionamiento.
* Paso 12: Instalamos el plugin serverless-add-api-key: ```npm i -g serverless-add-api-key```
* Paso 13: Añadimos api key en el serverless.yml y testeamos el API de nuevo.


## Instrucciones para ejecutar la API
Con una herramienta como cURL o Postman, podemos llamar a los siguientes endpoints:  
* GET - https://svwncifji6.execute-api.eu-west-1.amazonaws.com/dev/favouriteOrganization
* POST - https://svwncifji6.execute-api.eu-west-1.amazonaws.com/dev/favouriteOrganization (Para esta petición debemos adjuntar un body tipo json, con los campos "org_id" y "favourite_org_id", ambos de tipo string)  
Recordemos que, para ejecutar ambos métodos, será necesario incluir la cabecera ```x-api-key``` con el valor ```abcdefghijklmnopqrstuvwxyz1234567890```. En caso contrario, la api nos devolverá una respuesta 403 - Forbidden.
