FROM odoo:17.0

# Instalar las dependencias necesarias para compilar algunos paquetes de Python
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    python3-dev \
    gcc

# Establecer el directorio de trabajo
WORKDIR /odoo

# Copiar el archivo de configuración
COPY ./odoo.conf /etc/odoo/odoo.conf

# Copiar los módulos personalizados
COPY ./addons /mnt/extra-addons

# Instalar dependencias adicionales si es necesario
COPY ./requirements.txt /odoo/requirements.txt
RUN pip install -r /odoo/requirements.txt

# Exponer el puerto por defecto de Odoo
EXPOSE 8069 8071

# Comando por defecto para iniciar Odoo
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
