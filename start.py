import argparse
from linker import _search, claim_mail, slug
from dotenv import load_dotenv


parser = argparse.ArgumentParser()
parser.add_argument(
    'cmd',
    help='Commande à executer',
    choices=('search', 'extract')

)
parser.add_argument(
    '--engines',
    '-e',
    help='Moteurs de recherches à utiliser pour la recherche',
    default='01234'
)
parser.add_argument(
    '--search',
    '-S',
    help='Saisie de la recherche',
    default='Hello, world'
)
parser.add_argument(
    '--deep',
    '-d',
    help='Profondeur de la recherche',
    default=3,
    type=int
)
parser.add_argument(
    '--output',
    '-o',
    help='Nom du fichier de sortie des résultas de la recherche [les formats JSON et CSV sont supportés]',
    default=''
)

parser.add_argument(
    '--host',
    '-H',
    help='Lien du site d\'où les données doivent être extraites'
)
if __name__ == '__main__':
    load_dotenv()
    args = parser.parse_args()
    out = args.output if args.output else f'{slug(args.search)}:{args.engines}.csv'
    if args.cmd == 'search':
        _search(
            engines=args.engines,
            search=args.search,
            out=out,
            deep=args.deep
        )
    elif args.cmd == 'extract':
        r = claim_mail(args.host)
        print('Host : {} \nEmail : {}\nTel : {}'.format(args.host, *r))
