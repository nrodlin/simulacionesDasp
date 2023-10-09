# Simulaciones

## Comandos git

1) Genera un clave SSH usando la terminal en NoMachine: ssh-keygen -t ed25519 -C "NoMachine"
2) Copia la clave publica (ed25519.pub) en tu cuenta GitHub > Settings > SSH and GPG keys

3) Clona el repositorio

'git clone git@github.com:nrodlin/simulacionesDasp.git'

4) El repositorio se habrá clonado en la carpeta donde hayas ejecutado el git clone.

## Comandos git útiles (se ejecutan dentro del repositorio):

- git pull: actualiza el repositorio local (dentro del NoMachine) con el del servidor (copia de seguridad en gitHub)
- git add filename.py: Añade el archivo que indiques para incluirlo en el grupo de cambios que se van a etiquetar.
- git commit -m 'Comentario de que cambios has hecho': Etiqueta los cambios en los archivos que hayas modificado y añadido con git add
- git push: Sube los cambios etiquetas en git commit al servidor de GitHub

## DASP:

1) Para ejecutar una simulación, entra en la carpeta correspondiente (scaoSim, glaoSim): python glao.py params.py (bucle simulacion, parámetros simulacion respectivamente)
2) Otros comandos:
- daspctrl.py: interfaz para mostar gráficas simulación (tienes que ejecutar primero la simulación, darle a Connect y luego Get plots).
- daspbuilder.py: sirve para crear simulaciones. No tiene la misma estructura que las que te paso, pero si quieres hacer pruebas luego puedes fusionar formatos con un poco de cuidado.


