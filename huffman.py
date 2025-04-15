from bytestream import *


class HuffmanTree:
    def __init__(self, freq: int, char: str = None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(le caractère {self.char} possède une fréquence :{self.freq})"


def build_freqs(text: str) -> dict[str, int]:
    """
    Args :
        text : chaine de caractère à compresser
    Return :
        dict_letters : dictionnaire contenant le tuple clé-valeur → caractère et fréquence
    """
    dict_letters2freqs = {}

    for char in text:
        if char in dict_letters2freqs:
            dict_letters2freqs[char] += 1

        else:
            dict_letters2freqs[char] = 1

    return dict_letters2freqs


def build_huffman_tree(freqs: dict[str, int]) -> HuffmanTree:
    """
    Construit un arbre de Huffman en se basant syr un dictionnaire contenant les fréquences des caractères.
    Args :
        freqs : dictionnaire contenant les tuples (lettre, fréquence)

    Return :
        La racine de l'arbre de Huffman formé
    """
    # Créer une liste de nœuds pour chaque caractère chaque nœud est un sous-arbre
    nodes = []
    # parcourt par clé, valeur
    for char, freq in freqs.items():
        nodes.append(HuffmanTree(freq, char))

    # Continuer jusqu'à n'avoir qu'un seul nœud (la racine)
    while len(nodes) > 1:
        # Trier les nœuds par fréquence (du plus petit au plus grand)
        # ligne trouvée avec Copilot en demandant un tri de liste de tuple basé sur des entiers
        # on prend la clé de tri x et on trie selon les fréquences de x.
        nodes.sort(key=lambda x: x.freq)

        # Prendre les deux nœuds avec les plus petites fréquences
        left = nodes.pop(0)
        right = nodes.pop(0)

        # Créer un nouveau nœud parent avec ces deux nœuds comme enfants
        parent = HuffmanTree(
            freq=left.freq + right.freq,  # la somme des fréquences
            char=None,  # les nœuds internes n'ont pas de caractère
            left=left,  # enfant gauche
            right=right  # enfant droit
        )

        # Ajouter le nouveau nœud à la liste
        nodes.append(parent)

    # Retourner la racine de l'arbre (le seul nœud restant) → l'arbre de Huffman formé
    return nodes[0] if nodes else None


def build_encodings(tree: HuffmanTree) -> dict[str, str]:
    """
    Traduit un arbre de Huffman en un dictionnaire de codage.
    Args :
        tree : La racine de l'arbre de Huffman

    Return :
        Un dictionnaire associant chaque caractère à son code binaire
    """
    encodings = {}

    def recursive_parcours(node, code=""):
        if node.char is not None:
            encodings[node.char] = code
            # on "remonte" de profondeur si c'est une feuille
            return

        # Parcours récursif : gauche = 0, droite = 1
        if node.left:
            recursive_parcours(node.left, code + "0")
        if node.right:
            recursive_parcours(node.right, code + "1")

    # Lancer le parcours récursif depuis la racine
    recursive_parcours(tree)
    return encodings


def huffman_encode(plain: str, tree: HuffmanTree) -> bytes:
    """
    Compresse une chaîne de caractères en utilisant l'encodage de Huffman.

    Args :
        plain : La chaîne à compresser
        tree : L'arbre de Huffman à utiliser

    Return :
        Les données compressées sous forme de bytes
    """
    # Récupérer le dictionnaire d'encodage
    encodings = build_encodings(tree)

    # Encoder chaque caractère de la chaîne
    compressed = ""
    for char in plain:
        compressed += encodings[char]

    # Convertir la chaîne binaire en bytes
    return bin2bytes(compressed)


def huffman_decode(bytestream: bytes, tree: HuffmanTree) -> str:
    """
    Décompresse une chaîne de bytes en utilisant l'arbre de Huffman fourni en paramètre.

    Args :
        bytestream : Les données compressées sous forme de bytes
        tree : L'arbre de Huffman utilisé pour la compression

    Return :
        La chaîne décompressée
    """
    # Convertir les bytes en chaîne binaire
    compressed_chain = bytes2bin(bytestream)

    plain = ""
    # on part de la racine
    current_node = tree

    # Parcourir chaque bit de la chaîne binaire
    for bit in compressed_chain:
        # Descendre dans l'arbre
        if bit == '0':
            current_node = current_node.left
        else:  # bit == '1'
            current_node = current_node.right

        # Si on atteint une feuille
        if current_node.char is not None:
            # Ajouter le caractère à la chaîne décompressée
            plain += current_node.char
            # Retourner à la racine pour le prochain caractère
            current_node = tree
    return plain
