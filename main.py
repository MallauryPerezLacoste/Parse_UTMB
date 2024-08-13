import parse as p
import sys


if __name__ == "__main__":
    if(len(sys.argv)<=2):
        if(len(sys.argv)==2):
            if sys.argv[1]=="-h":
                print("arg1 = url de la course UTMB, arg2 UTMB index du premier de la course")
            else:
                print("Manque d'argument")
        else:
            print("Manque d'argument")    
    else:
        try:
            float(sys.argv[2])  # Essaye de convertir en float
        except ValueError:
            print("UTMB index max entré non valide")
            sys.exit(0)
        if(p.generale(sys.argv[1], sys.argv[2])==-1):
            print("Erreur dans l'annalyse de la course")
            sys.exit(0)
        print("Exécuté avec succès")
    sys.exit(0)