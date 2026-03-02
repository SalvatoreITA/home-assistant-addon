FROM dadoum/anisette-v3-server:latest

USER root

# Copia lo script di avvio
COPY run.sh /run.sh

# Rimuove i ritorni a capo di Windows e dà i permessi
RUN sed -i 's/\r$//' /run.sh && chmod a+x /run.sh

# Sovrascrive l'avvio originale
ENTRYPOINT [ "/run.sh" ]
