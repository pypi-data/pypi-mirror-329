'''
Author : Vincent LE DOZE
Date : 31/05/23

This file contains all constants for excel parsing.

'''

# Variables globales ==========================================================================
# Tags for nodes & links -----------------------------------------------
TAG_SHEET = 'tags'
TAG_NAME, TAG_TYPE, TAG_TAGS, TAG_IS_PALETTE, TAG_COLORMAP, TAG_COLOR =\
    'tag_name', 'tag_type', 'tags', 'is_palette', 'colormap', 'tag_color'
TAG_SHEET_COLS = [
    TAG_NAME, TAG_TYPE, TAG_TAGS, TAG_IS_PALETTE, TAG_COLORMAP, TAG_COLOR]
TAG_TYPE_DATA = 'dataTags'
TAG_TYPE_FLUX = 'fluxTags'
TAG_TYPE_NODE = 'nodeTags'
TAG_TYPE_LEVEL = 'levelTags'

# Tags for nodes --------------------------------------------------------
NODE_TYPE = 'Type de noeud'
NODE_TYPE_PRODUCT = 'produit'
NODE_TYPE_SECTOR = 'secteur'
NODE_TYPE_EXCHANGE = 'echange'

# Tags for AFM module --------------------------------------------------
DATA_TYPE_LABEL = 'Type de donnée'
DATA_COMPUTED = 'Donnée calculée'
DATA_COLLECTED = 'Donnée collectée'

# Node description sheet -----------------------------------------------
NODES_SHEET = 'nodes'
PRODUCTS_SHEET = 'dim_products'
SECTORS_SHEET = 'dim_sectors'
EXCHANGES_SHEET = 'exchanges'

NODES_LEVEL = 'level'
NODES_NODE = 'node'
NODES_MAT_BALANCE = 'mat_balance'
NODES_SANKEY = 'sankey'
NODES_COLOR = 'color'
NODES_DEFINITIONS = 'definitions'
NODES_SHEET_COLS = [
    NODES_LEVEL, NODES_NODE, NODES_MAT_BALANCE,
    NODES_SANKEY, NODES_COLOR, NODES_DEFINITIONS
]

# Data description sheets ----------------------------------------------
DATA_SHEET = 'data'
DATA_ORIGIN = 'origin'
DATA_DESTINATION = 'destination'
DATA_VALUE = 'value'
DATA_QUANTITY = 'quantity'
DATA_NATURAL_UNIT = 'natural_unit'
DATA_FACTOR = 'factor'
DATA_UNCERT = 'uncert'
DATA_SOURCE = 'sources'
DATA_HYPOTHESIS = 'hypotheses'
DATA_SHEET_COLS_1 = [DATA_ORIGIN, DATA_DESTINATION]
DATA_SHEET_COLS_2 = \
    [DATA_VALUE, DATA_QUANTITY, DATA_NATURAL_UNIT, DATA_FACTOR,
     DATA_UNCERT, DATA_SOURCE, DATA_HYPOTHESIS]
DATA_SHEET_COLS = DATA_SHEET_COLS_1 + DATA_SHEET_COLS_2

DEFAULT_SIGMA_RELATIVE = 0.1
DEFAULT_SIGMA_PERCENT = DEFAULT_SIGMA_RELATIVE*100.0

# Flux description sheet -----------------------------------------------
FLUX_SHEET = 'flux'
FLUX_SHEET_COLS = [DATA_ORIGIN, DATA_DESTINATION]

IO_SHEET = 'input_output'
TER_SHEET = 'ter'
IO_DATA_SHEET = 'input_output_data'

# Constraint description sheets ----------------------------------------
MIN_MAX_SHEET = 'min_max'
MIN_MAX_ORIGIN = 'origin'
MIN_MAX_DESTINATION = 'destination'
MIN_MAX_MIN = 'min'
MIN_MAX_MAX = 'max'
MIN_MAX_MIN_QUANTITY = 'min_quantity'
MIN_MAX_MAX_QUANTITY = 'max_quantity'
MIN_MAX_NATURAL_UNIT = 'natural_unit'
MIN_MAX_FACTOR = 'factor'
MIN_MAX_SOURCE = 'sources'
MIN_MAX_HYPOTHESIS = 'hypotheses'
MIN_MAX_SHEET_COLS_1 = [
    MIN_MAX_ORIGIN, MIN_MAX_DESTINATION]
MIN_MAX_SHEET_COLS_2 = [
    MIN_MAX_MIN, MIN_MAX_MAX,
    MIN_MAX_MIN_QUANTITY, MIN_MAX_MAX_QUANTITY,
    MIN_MAX_NATURAL_UNIT, MIN_MAX_FACTOR,
    MIN_MAX_SOURCE, MIN_MAX_HYPOTHESIS]
MIN_MAX_SHEET_COLS = MIN_MAX_SHEET_COLS_1 + MIN_MAX_SHEET_COLS_2

CONSTRAINTS_SHEET = 'constraints'
CONSTRAINT_ID = 'id'
CONSTRAINT_ORIGIN = 'origin'
CONSTRAINT_DESTINATION = 'destination'
CONSTRAINT_EQ = 'eq = 0'
CONSTRAINT_INEQ_INF = 'eq <= 0'
CONSTRAINT_INEQ_SUP = 'eq >= 0'
CONSTRAINT_TRADUCTION = 'traduction'
CONSTRAINT_SOURCE = 'source'
CONSTRAINT_HYPOTHESIS = 'hypotheses'
CONSTRAINT_SHEET_COLS_1 = [
    CONSTRAINT_ID, CONSTRAINT_ORIGIN, CONSTRAINT_DESTINATION]
CONSTRAINT_SHEET_COLS_2 = [
    CONSTRAINT_EQ, CONSTRAINT_INEQ_INF, CONSTRAINT_INEQ_SUP,
    CONSTRAINT_TRADUCTION, CONSTRAINT_SOURCE, CONSTRAINT_HYPOTHESIS]
CONSTRAINT_SHEET_COLS = CONSTRAINT_SHEET_COLS_1 + CONSTRAINT_SHEET_COLS_2

DATA_UNCERTAINTY_LABEL = 'Incertitudes données'
UNCERTAINTY_LABEL = 'Incertitudes réconciliées'
UNCERT_1_PRCT_LABEL = '< 1%'
UNCERT_5_PRCT_LABEL = '< 5%'
UNCERT_10_PRCT_LABEL = '< 10%'
UNCERT_25_PRCT_LABEL = '< 25%'
UNCERT_50_PRCT_LABEL = '< 50%'
UNCERT_50_MORE_PRCT_LABEL = '> 50%'

RESULTS_SHEET = 'results'
RESULTS_ORIGIN = 'origin'
RESULTS_DESTINATION = 'destination'
RESULTS_VALUE = 'value'
RESULTS_FREE_MIN = 'free min'  # Si variable libre (indeterminée), valeur min de l'intervalle
RESULTS_FREE_MAX = 'free max'  # Si variable libre (indeterminée), valeur max de l'intervalle
RESULTS_SHEET_COLS_1 = [RESULTS_ORIGIN, RESULTS_DESTINATION]
RESULTS_SHEET_COLS_2 = [RESULTS_VALUE, RESULTS_FREE_MIN, RESULTS_FREE_MAX]
RESULTS_SHEET_COLS = RESULTS_SHEET_COLS_1 + RESULTS_SHEET_COLS_2

ANALYSIS_SHEET = 'analysis'
ANALYSIS_VALUE_IN = 'value in'
ANALYSIS_VALUE_IN_SIGMA = 'sigma in'
ANALYSIS_VALUE_IN_SIGMA_PRCT = 'sigma in %'
ANALYSIS_VALUE_MIN_IN = 'min in'
ANALYSIS_VALUE_MAX_IN = 'max in'
ANALYSIS_NB_SIGMAS = 'nb_sigmas'  # Eloignement en sigma de la valeur resultat / donnée entrée
ANALYSIS_CLASSIF = 'classif'  # Mesurée / Redondandes / Determinable / Indeterminable (libre)
ANALYSIS_AI = 'Ai'  # Liste de lignes dans lesquelles la donnée est impliquée dans la matrice de contrainte.
ANALYSIS_SHEET_COLS_1 = [RESULTS_ORIGIN, RESULTS_DESTINATION]
ANALYSIS_SHEET_COLS_2 = [
    RESULTS_VALUE, RESULTS_FREE_MIN, RESULTS_FREE_MAX,
    ANALYSIS_VALUE_IN, ANALYSIS_VALUE_IN_SIGMA, ANALYSIS_VALUE_IN_SIGMA_PRCT,
    ANALYSIS_VALUE_MIN_IN, ANALYSIS_VALUE_MAX_IN, ANALYSIS_NB_SIGMAS,
    ANALYSIS_CLASSIF]  # , ANALYSIS_AI]
ANALYSIS_SHEET_COLS = ANALYSIS_SHEET_COLS_1 + ANALYSIS_SHEET_COLS_2

UNCERTAINTY_SHEET = 'uncertainty'
UNCERTAINTY_ORIGIN = RESULTS_ORIGIN
UNCERTAINTY_DESTINATION = RESULTS_DESTINATION
UNCERTAINTY_MC_MU_IN = 'MC mu in'  # Valeur Moyenne tirage monté-carlo avant reconcilliation
UNCERTAINTY_MC_STD_IN = 'MC std in'  # Ecart-type tirage monté-carlo avant reconcilliation
UNCERTAINTY_MC_MU = 'MC mu'  # Valeur Moyenne tirage monté-carlo après reconcilliation
UNCERTAINTY_MC_STD = 'MC std'  # Ecart-type tirage monté-carlo après reconcilliation
UNCERTAINTY_MC_MIN = 'MC min'
UNCERTAINTY_MC_MAX = 'MC max'
UNCERTAINTY_MC_P0 = 'MC p0'
UNCERTAINTY_MC_P5 = 'MC p5'
UNCERTAINTY_MC_P10 = 'MC p10'
UNCERTAINTY_MC_P20 = 'MC p20'
UNCERTAINTY_MC_P30 = 'MC p30'
UNCERTAINTY_MC_P40 = 'MC p40'
UNCERTAINTY_MC_P50 = 'MC p50'
UNCERTAINTY_MC_P60 = 'MC p60'
UNCERTAINTY_MC_P70 = 'MC p70'
UNCERTAINTY_MC_P80 = 'MC p80'
UNCERTAINTY_MC_P90 = 'MC p90'
UNCERTAINTY_MC_P95 = 'MC p95'
UNCERTAINTY_MC_P100 = 'MC p100'
UNCERTAINTY_MC_HIST0 = 'MC hist0'
UNCERTAINTY_MC_HIST1 = 'MC hist1'
UNCERTAINTY_MC_HIST2 = 'MC hist2'
UNCERTAINTY_MC_HIST3 = 'MC hist3'
UNCERTAINTY_MC_HIST4 = 'MC hist4'
UNCERTAINTY_MC_HIST5 = 'MC hist5'
UNCERTAINTY_MC_HIST6 = 'MC hist6'
UNCERTAINTY_MC_HIST7 = 'MC hist7'
UNCERTAINTY_MC_HIST8 = 'MC hist8'
UNCERTAINTY_MC_HIST9 = 'MC hist9'
UNCERTAINTY_SHEET_PCOLS = [
    UNCERTAINTY_MC_P0,
    UNCERTAINTY_MC_P5,
    UNCERTAINTY_MC_P10,
    UNCERTAINTY_MC_P20,
    UNCERTAINTY_MC_P30,
    UNCERTAINTY_MC_P40,
    UNCERTAINTY_MC_P50,
    UNCERTAINTY_MC_P60,
    UNCERTAINTY_MC_P70,
    UNCERTAINTY_MC_P80,
    UNCERTAINTY_MC_P90,
    UNCERTAINTY_MC_P95,
    UNCERTAINTY_MC_P100]
UNCERTAINTY_SHEET_HCOLS = [
    UNCERTAINTY_MC_HIST0,
    UNCERTAINTY_MC_HIST1,
    UNCERTAINTY_MC_HIST2,
    UNCERTAINTY_MC_HIST3,
    UNCERTAINTY_MC_HIST4,
    UNCERTAINTY_MC_HIST5,
    UNCERTAINTY_MC_HIST6,
    UNCERTAINTY_MC_HIST7,
    UNCERTAINTY_MC_HIST8,
    UNCERTAINTY_MC_HIST9]
UNCERTAINTY_SHEET_COLS = [
    UNCERTAINTY_ORIGIN,
    UNCERTAINTY_DESTINATION,
    UNCERTAINTY_MC_MU_IN,
    UNCERTAINTY_MC_STD_IN,
    UNCERTAINTY_MC_MU,
    UNCERTAINTY_MC_STD,
    UNCERTAINTY_MC_MIN,
    UNCERTAINTY_MC_MAX] + UNCERTAINTY_SHEET_PCOLS + UNCERTAINTY_SHEET_HCOLS

SIMULATIONS_SHEET = 'simulations'

CONVERSIONS_SHEET = 'conversions'
CONVERSIONS_LOCATION = 'location'
CONVERSIONS_PRODUCT = 'product'
CONVERSIONS_COMMENTARY = 'commentary'
CONVERSIONS_NATURAL_UNIT = 'natural unit'
CONVERSIONS_FACTOR = 'factor'
CONVERSIONS_FACTOR_INV = 'factor_inv'
CONVERSIONS_SHEET_COLS = [
    CONVERSIONS_LOCATION, CONVERSIONS_PRODUCT, CONVERSIONS_NATURAL_UNIT,
    CONVERSIONS_FACTOR, CONVERSIONS_FACTOR_INV, CONVERSIONS_COMMENTARY]

# Possible names for sheets of I/O Excel file --------------------------------------
# Language
LANG_FR = 0  # First value is French
LANG_EN = 1  # Second value is always English, etc.

# All following names (sheet & cols) are list of std name as [French, English]
# Does not apply for RE (RegEx references)
DICT_OF_SHEET_NAMES = {
    TAG_SHEET: ['Etiquettes', 'Tags'],

    NODES_SHEET: ['Noeuds', 'Nodes'],
    PRODUCTS_SHEET: ['Produits', 'Products'],
    SECTORS_SHEET:  ['Secteurs', 'Sectors'],
    EXCHANGES_SHEET:  ['Echanges', 'Exchanges'],

    FLUX_SHEET: ['Liste des flux', 'Flux list'],
    TER_SHEET: ['Table emplois ressources', 'Supply-use table'],
    IO_SHEET: ['Table entrées-sorties', 'Input-Output table'],
    IO_DATA_SHEET: ['Table entrée sortie avec données', 'Input-Output table with datas'],

    DATA_SHEET: ['Valeurs', 'Values'],
    MIN_MAX_SHEET: ['Min Max', 'Min Max'],
    CONSTRAINTS_SHEET: ['Contraintes', 'Constraints'],

    RESULTS_SHEET: ['Résultats', 'Results'],
    ANALYSIS_SHEET: ['Analyses des résultats', 'Results analysis'],
    UNCERTAINTY_SHEET: ['Analyses d\'incertitudes', 'Uncertainty analysis'],
    SIMULATIONS_SHEET: ['Simulations', 'Simulations'],

    CONVERSIONS_SHEET: ['Conversions', 'Conversions'],

    'proxy': ['proxi', 'proxy'],
    'pflow': ['flow'],
    'psect': [],
    'geo': ['geo']
}

# Format RegEx for sheet name mathcing
DICT_OF_SHEET_NAMES__RE = {
    TAG_SHEET: ['e?tiquettes?', 'tags?', TAG_SHEET],

    NODES_SHEET: ['noeuds.*', 'nodes.*', NODES_SHEET],
    PRODUCTS_SHEET: ['(dim )?produits.*', '(dim )?products?', 'dim_products', PRODUCTS_SHEET],
    SECTORS_SHEET:  ['(dim )?secteurs.*', '(dim )?sectors?', 'dim_sectors', SECTORS_SHEET],
    EXCHANGES_SHEET:  ['e?changes?( territoires?)?', 'exchanges?', EXCHANGES_SHEET],

    FLUX_SHEET: ['liste des flux', 'flux list', FLUX_SHEET],
    TER_SHEET: [
        'table emplois?[ \-]?ressources?',  # noqa
        'supply[\- ]?use table',  # noqa
        'structure( des flux)?',
        'ter.*',
        'flux.*',
        TER_SHEET],
    IO_SHEET: [
        'table entr[eé]?es?[ -]?sorties?',
        'input[_\- ]?output[ ]*(table)?',  # noqa
        IO_SHEET],
    IO_DATA_SHEET: [
        'table entr[ée]?es?[ -]?sorties?( avec )?donnees?',
        'input[_\- ]?output table( with )?datas?',  # noqa
        IO_DATA_SHEET],

    DATA_SHEET: [
        'valeurs?( de flux)?',
        'values?',
        'donnee?s?',
        'data',
        'donn',
        DATA_SHEET],
    MIN_MAX_SHEET: ['min[ _]max', MIN_MAX_SHEET],
    CONSTRAINTS_SHEET: ['contraintes?', 'constraints?', CONSTRAINTS_SHEET],

    RESULTS_SHEET: ['resultats?', 'results?', RESULTS_SHEET],
    # ANALYSIS_SHEET: ['analyses?( des resultats?)?', '(results )?analysis', ANALYSIS_SHEET],
    UNCERTAINTY_SHEET: ['analyses? d\'incertitudes?', 'uncertainty analysis', UNCERTAINTY_SHEET],
    SIMULATIONS_SHEET: ['simulations?', SIMULATIONS_SHEET],

    CONVERSIONS_SHEET: ['conversions?', 'convert', CONVERSIONS_SHEET],

    'proxy': ['prox[yi]'],
    'pflow': ['flow'],
    'psect': [],
    'geo': ['geo']
}

# Possible names for existing columns for each sheets of Excel file
# All following names are list of std name as [French, English]
# Does not apply for RE (RegEx references)
DICT_OF_COLS_NAMES = {
    TAG_SHEET: {
        TAG_NAME: ['Nom du groupe d\'étiquette', 'Tags group name'],  # *
        TAG_TYPE: ['Type d\'étiquette', 'Tags type'],  # *
        TAG_TAGS: ['Etiquettes', 'Tags'],  # *
        TAG_IS_PALETTE: ['Palette visible', 'Visible colormap'],
        TAG_COLORMAP: ['Palette de couleur', 'Colormap'],
        TAG_COLOR: ['Couleurs', 'Colors']
    },
    NODES_SHEET: {
        NODES_LEVEL: ['Niveau d\'agrégation', 'Aggregation level'],  # int
        NODES_NODE: ['Noeuds', 'Nodes'],  # *
        NODES_MAT_BALANCE: ['Equilibre entrée-sortie', 'Input-output balance'],  # int
        NODES_SANKEY: ['Affichage sur le diagramme de Sankey', 'Sankey'],
        NODES_COLOR: ['Couleur', 'Color'],
        NODES_DEFINITIONS: ['Définitions', 'Definition']
    },
    PRODUCTS_SHEET: {
        NODES_LEVEL: ['Niveau d\'agrégation', 'Aggregation level'],  # int
        NODES_NODE: ['Noeuds', 'Nodes', 'Produits', 'Products'],  # *
        NODES_MAT_BALANCE: ['Equilibre entrée-sortie', 'Input-output balance'],  # int
        NODES_SANKEY: ['Affichage sur le diagramme de Sankey', 'Sankey'],
        NODES_COLOR: ['Couleur', 'Color'],
        NODES_DEFINITIONS: ['Définitions', 'Definition']
    },
    SECTORS_SHEET: {
        NODES_LEVEL: ['Niveau d\'agrégation', 'Aggregation level'],  # int
        NODES_NODE: ['Noeuds', 'Nodes', 'Secteurs', 'Sectors'],  # *
        NODES_MAT_BALANCE: ['Equilibre entrée-sortie', 'Input-output balance'],  # int
        NODES_SANKEY: ['Affichage sur le diagramme de Sankey', 'Sankey'],
        NODES_COLOR: ['Couleur', 'Color'],
        NODES_DEFINITIONS: ['Définitions', 'Definition']
    },
    EXCHANGES_SHEET: {
        NODES_LEVEL: ['Niveau d\'agrégation', 'Aggregation level'],  # * int
        NODES_NODE: ['Noeuds', 'Nodes', 'Echanges', 'Exchanges'],  # *
        NODES_SANKEY: ['Affichage sur le diagramme de Sankey', 'Sankey'],
        NODES_COLOR: ['Couleur', 'Color'],
        NODES_DEFINITIONS: ['Définitions', 'Definition']
    },
    DATA_SHEET: {
        DATA_ORIGIN: ['Origine', 'Origin'],
        DATA_DESTINATION: ['Destination', 'Target'],
        DATA_VALUE: ['Valeur', 'Value'],
        DATA_QUANTITY: ['Quantité naturelle', 'Quantity'],
        DATA_NATURAL_UNIT: ['Unité naturelle', 'Unit'],
        DATA_FACTOR: ['Facteur de conversion', 'Factor'],
        DATA_UNCERT: ['Incertitude relative', 'Relative Uncertainty'],
        DATA_SOURCE: ['Source', 'Source'],
        DATA_HYPOTHESIS: ['Hypothèse', 'Hypothesis']
    },
    MIN_MAX_SHEET: {
        MIN_MAX_ORIGIN: ['Origine', 'Origin'],  # *
        MIN_MAX_DESTINATION: ['Destination', 'Target'],  # *
        MIN_MAX_MIN: ['Minimum', 'Minimum'],  # float
        MIN_MAX_MAX: ['Maximum', 'Maximum'],  # float
        MIN_MAX_MIN_QUANTITY: ['Minimum en quantité naturelle', 'Minimun in quantity'],  # float
        MIN_MAX_MAX_QUANTITY: ['Maximum en quantité naturelle', 'Maximum in quantity'],  # float
        MIN_MAX_NATURAL_UNIT: ['Unité naturelle', 'Unity'],  # *
        MIN_MAX_FACTOR: ['Facteur de conversion', 'Factor'],  # float
        MIN_MAX_SOURCE: ['Source', 'Source'],  # *
        MIN_MAX_HYPOTHESIS: ['Hypothèse', 'Hypothesis']  # *
    },
    CONSTRAINTS_SHEET: {
        CONSTRAINT_ID: ['ID', 'ID'],
        CONSTRAINT_ORIGIN: ['Origine', 'origin'],
        CONSTRAINT_DESTINATION: ['Destination', 'Target'],
        CONSTRAINT_EQ: ['Equation d\'égalité (eq = 0)', 'Equality equation (eq = 0)'],
        CONSTRAINT_INEQ_INF: [
            'Equation d\'inégalité borne haute (ineq <= 0)',
            'Inequality equation, lower boundary (ineq <= 0)'],
        CONSTRAINT_INEQ_SUP: [
            'Equation d\'inégalité borne basse (ineq >= 0)',
            'Inequality equation, upper boundary (ineq >= 0)'],
        CONSTRAINT_SOURCE: ['Source', 'Source'],
        CONSTRAINT_HYPOTHESIS: ['Hypothèses', 'Hypothesis'],
        CONSTRAINT_TRADUCTION: ['Traduction', 'Translation']
    },
    RESULTS_SHEET: {
        RESULTS_ORIGIN: ['Origine', 'Origin'],  # *
        RESULTS_DESTINATION: ['Destination', 'Target'],  # *
        RESULTS_VALUE: ['Valeur reconciliée', 'Reconciled value'],  # *
        RESULTS_FREE_MIN: ['Borne inférieure', 'Lower boundary'],
        RESULTS_FREE_MAX: ['Borne supérieure', 'Upper boundary']
    },
    ANALYSIS_SHEET: {
        RESULTS_ORIGIN: ['Origine', 'Origin'],  # *
        RESULTS_DESTINATION: ['Destination', 'Target'],  # *
        RESULTS_VALUE: ['Valeur reconciliée', 'Reconciled value'],  # float
        RESULTS_FREE_MIN: ['Borne inférieure', 'Lower boundary'],  # float
        RESULTS_FREE_MAX: ['Borne supérieure', 'Upper boundary'],  # float
        ANALYSIS_VALUE_IN: ['Valeur non-réconciliée', 'Unreconciled value'],  # float
        ANALYSIS_VALUE_MIN_IN: [
            'Borne inférieure non-réconciliée',
            'Unreconciled lower boundary'],  # float
        ANALYSIS_VALUE_MAX_IN: [
            'Borne supérieure non-réconciliée',
            'Unreconciled upper boundary'],  # float
        ANALYSIS_VALUE_IN_SIGMA: [
            'Incertitude absolue non-réconciliée',
            'Unreconciled absolute uncertainty'],  # float
        ANALYSIS_VALUE_IN_SIGMA_PRCT: [
            'Incertitude relative non-réconciliée',
            'Unreconciled relative uncertainty'],  # float
        ANALYSIS_NB_SIGMAS: [
            'Eloignement de la valeur réconciliée par rapport à la valeur non-réconciliée',
            'Distance of the reconciled value compared to the unreconciled value'],  # float
        ANALYSIS_AI: ['Ai', 'Ai'],
        ANALYSIS_CLASSIF: ['Type de variable', 'Variable type']  # *
    },
    UNCERTAINTY_SHEET: {
        RESULTS_ORIGIN: ['Origine', 'Origin'],
        RESULTS_DESTINATION: ['Destination', 'Target']
    },
    CONVERSIONS_SHEET: {
        CONVERSIONS_LOCATION: ['Unité locale', 'Local unit'],
        CONVERSIONS_PRODUCT:  ['Produits', 'Products'],
        CONVERSIONS_NATURAL_UNIT: ['Unité naturelle', 'Natural unit'],
        CONVERSIONS_FACTOR: [
            'Facteur de conversion (Unité locale / Unité naturelle)',
            'Conversion factor (Local unit / Natural unit)'],
        CONVERSIONS_FACTOR_INV: [
            'Inverse facteur de conversion (Unité naturelle / Unité locale)',
            'Inversed conversion factor (Natural unit / Local unit)'],
        CONVERSIONS_COMMENTARY: ['Commentaires', 'Commentaries']
    }
}

# Regular expressions for possible names for existing columns for each sheets of I/O Excel file
DICT_OF_COLS_NAMES__RE = {
    TAG_SHEET: {
        TAG_NAME: ['(tag)?s?.*name', 'nom.*(etiquette)?s?', TAG_NAME],  # *
        TAG_TYPE: ['(tag)?s?.*type', 'type.*(etiquette)?s?', TAG_TYPE],  # *
        TAG_TAGS: ['tags?', 'etiquettes?', TAG_TAGS],  # *
        TAG_IS_PALETTE: ['palette', 'palette visible', TAG_IS_PALETTE],
        TAG_COLORMAP: ['colormap', 'palette de couleur', TAG_COLORMAP],
        TAG_COLOR: ['colors?', 'couleurs?', TAG_COLOR]
    },
    NODES_SHEET: {
        NODES_LEVEL: [
            'niveaux?.*agg?regation',
            'agg?regg?ations?[ \-]*levels?',  # noqa
            'niveaux?', 'levels?', 'hierarchie', NODES_LEVEL],  # * int
        NODES_NODE: [
            'noeuds?', 'nœuds?', 'liste des produits?', 'liste des secteurs?',
            'liste des echanges?', 'elements?', 'noms?', NODES_NODE],  # *
        NODES_MAT_BALANCE: [
            'equilibre entrees?-sorties?', 'input[\- ]?output balance',  # noqa
            'equilibre matiere.*', 'bilan matieres?.*', 'contraintes? de conservation de la masse',
            'constraints?', 'mat_?balance', NODES_MAT_BALANCE],  # int
        NODES_SANKEY: ['affichage sur le diagramme de sankey', 'sankey[ ?]*', NODES_SANKEY],
        NODES_COLOR: ['couleur', 'color', NODES_COLOR],
        NODES_DEFINITIONS: ['definitions?', NODES_DEFINITIONS]
    },
    PRODUCTS_SHEET: {
        NODES_LEVEL: [
            'niveaux?.*agg?regation',
            'agg?regg?ations?[ \-]*levels?',  # noqa
            'niveaux?', 'levels?', 'hierarchie', NODES_LEVEL],  # * int
        NODES_NODE: [
            'produits?', 'products?', 'noeuds?', 'nœuds?',
            'liste des produits?', 'liste des secteurs?', 'liste des echanges?',
            'elements?', 'noms?', NODES_NODE],  # *
        NODES_MAT_BALANCE: [
            'equilibre entrees?-sorties?', 'input[\- ]?output balance',  # noqa
            'equilibre matiere.*', 'bilan matieres?.*', 'contraintes? de conservation de la masse',
            'constraints?', 'mat_?balance', NODES_MAT_BALANCE],  # int
        NODES_SANKEY: ['affichage sur le diagramme de sankey', 'sankey[ ?]*', NODES_SANKEY],
        NODES_COLOR: ['couleur', 'color', NODES_COLOR],
        NODES_DEFINITIONS: ['definitions?', NODES_DEFINITIONS]
    },
    SECTORS_SHEET: {
        NODES_LEVEL: [
            'niveaux?.*agg?regation',
            'agg?regg?ations?[ \-]*levels?',  # noqa
            'niveaux?', 'levels?', 'hierarchie', NODES_LEVEL],  # * int
        NODES_NODE: [
            'secteurs?', 'sectors?', 'noeuds?', 'nœuds?',
            'liste des produits?', 'liste des secteurs?', 'liste des echanges?',
            'elements?', 'noms?', NODES_NODE],  # *
        NODES_MAT_BALANCE: [
            'equilibre entrees?-sorties?', 'input[\- ]?output balance',   # noqa
            'equilibre matiere.*', 'bilan matieres?.*', 'contraintes? de conservation de la masse',
            'constraints?', 'mat_?balance', NODES_MAT_BALANCE],  # int
        NODES_SANKEY: ['affichage sur le diagramme de sankey', 'sankey[ ?]*', NODES_SANKEY],
        NODES_COLOR: ['couleur', 'color', NODES_COLOR],
        NODES_DEFINITIONS: ['definitions?', NODES_DEFINITIONS]
    },
    EXCHANGES_SHEET: {
        NODES_LEVEL: [
            'niveaux?.*agg?regation',
            'agg?regg?ations?[ \-]*levels?',  # noqa
            'niveaux?', 'levels?', 'hierarchie', NODES_LEVEL],  # * int
        NODES_NODE: [
            'echanges?', 'exchanges?', 'noeuds?', 'nœuds?',
            'liste des produits?', 'liste des secteurs?', 'liste des echanges?',
            'elements?', 'noms?', NODES_NODE],  # *
        NODES_SANKEY: ['affichage sur le diagramme de sankey', 'sankey[ ?]*', NODES_SANKEY],
        NODES_COLOR: ['couleur', 'color', NODES_COLOR],
        NODES_DEFINITIONS: ['definitions?', NODES_DEFINITIONS]
    },
    DATA_SHEET: {
        DATA_ORIGIN: ['origine?', DATA_ORIGIN],
        DATA_DESTINATION: ['destination', 'target', DATA_DESTINATION],
        DATA_VALUE: ['valeur.*', 'value.*', DATA_VALUE],
        DATA_QUANTITY: ['quantite naturelle', 'quantity', DATA_QUANTITY],
        DATA_NATURAL_UNIT: ['unite naturelle', 'unit', DATA_NATURAL_UNIT],
        DATA_FACTOR: ['facteur de conversion', 'factor', DATA_FACTOR],
        DATA_UNCERT: ['incertitude( relative)?', '(relative )?uncertainty', DATA_UNCERT],
        DATA_SOURCE: ['sources?', DATA_SOURCE],
        DATA_HYPOTHESIS: ['hypotheses?', 'hypothesis', DATA_HYPOTHESIS]
    },
    MIN_MAX_SHEET: {
        MIN_MAX_ORIGIN: ['origine?', MIN_MAX_ORIGIN],
        MIN_MAX_DESTINATION: ['destination', 'target', MIN_MAX_DESTINATION],
        MIN_MAX_MIN: ['minimum( en quantite? de re?fe?rence)?', MIN_MAX_MIN],
        MIN_MAX_MAX: ['maximum( en quantite? de re?fe?rence)?', MIN_MAX_MAX],
        MIN_MAX_MIN_QUANTITY: ['minimum en quantite naturelle', 'minimum in quantity', MIN_MAX_MIN_QUANTITY],
        MIN_MAX_MAX_QUANTITY: ['maximum en quantite naturelle', 'maximum in quantity', MIN_MAX_MAX_QUANTITY],
        MIN_MAX_NATURAL_UNIT: ['unite naturelle', 'unity', MIN_MAX_NATURAL_UNIT],
        MIN_MAX_FACTOR: ['facteur de conversion', 'factor', MIN_MAX_FACTOR],
        MIN_MAX_SOURCE: ['sources?', MIN_MAX_SOURCE],
        MIN_MAX_HYPOTHESIS: ['hypotheses?', 'hypothesis', MIN_MAX_HYPOTHESIS]
    },
    CONSTRAINTS_SHEET: {
        CONSTRAINT_ID: ['id', 'identifiant', CONSTRAINT_ID],
        CONSTRAINT_ORIGIN: ['origine?', CONSTRAINT_ORIGIN],
        CONSTRAINT_DESTINATION: ['destination', 'target', CONSTRAINT_DESTINATION],
        CONSTRAINT_EQ: ['.*[(]?eq[ ]*=[ ]*0[)]?', CONSTRAINT_EQ],
        CONSTRAINT_INEQ_INF: ['.*[(]?(in)?eq[ ]*<=[ ]*0[)]?', CONSTRAINT_INEQ_INF],
        CONSTRAINT_INEQ_SUP: ['.*[(]?(in)?eq[ ]*>=[ ]*0[)]?', CONSTRAINT_INEQ_SUP],
        CONSTRAINT_SOURCE: ['sources?', CONSTRAINT_SOURCE],
        CONSTRAINT_HYPOTHESIS: ['hypotheses?', 'hypothesis', CONSTRAINT_HYPOTHESIS],
        CONSTRAINT_TRADUCTION: ['traductions?', 'translation', CONSTRAINT_TRADUCTION]
    },
    RESULTS_SHEET: {
        RESULTS_ORIGIN: ['origine?', RESULTS_ORIGIN],
        RESULTS_DESTINATION: ['destination', 'target', RESULTS_DESTINATION],
        RESULTS_VALUE: ['valeur reconciliee', 'reconcilied value', 'valeur de sortie du modele', RESULTS_VALUE],
        RESULTS_FREE_MIN: ['borne inferieure( des variables libres)?', 'lower boundary', RESULTS_FREE_MIN],
        RESULTS_FREE_MAX: ['borne superieure( des variables libres)?', 'upper boundary', RESULTS_FREE_MAX]
    },
    ANALYSIS_SHEET: {
        RESULTS_ORIGIN: ['origine?', RESULTS_ORIGIN],
        RESULTS_DESTINATION: ['destination', 'target', RESULTS_DESTINATION],
        RESULTS_VALUE: [
            'valeur re?conciliee?',
            'reconciled value',
            'valeur de sortie du modele',
            RESULTS_VALUE],
        RESULTS_FREE_MIN: [
            'borne inferieure( des variables libres)?',
            'lower boundary', RESULTS_FREE_MIN],
        RESULTS_FREE_MAX: [
            'borne superieure( des variables libres)?',
            'upper boundary',
            RESULTS_FREE_MAX],
        ANALYSIS_VALUE_IN: [
            'valeur non-re?conciliee?',
            'unreconciled value',
            'valeur d\'entree',
            ANALYSIS_VALUE_IN],
        ANALYSIS_VALUE_MIN_IN: [
            'borne infe?rieure non-re?conciliee?',
            'unreconciled lower boundary',
            'minimum d\'entree',
            ANALYSIS_VALUE_MIN_IN],
        ANALYSIS_VALUE_MAX_IN: [
            'borne supe?rieure non-re?conciliee?',
            'unreconciled upper boundary',
            'maximum d\'entree',
            ANALYSIS_VALUE_MAX_IN],
        ANALYSIS_VALUE_IN_SIGMA: [
            'incertitude absolue non-re?conciliee?',
            'unreconciled absolute uncertainty',
            'incertitude d\'entree',
            ANALYSIS_VALUE_IN_SIGMA],
        ANALYSIS_VALUE_IN_SIGMA_PRCT: [
            'incertitude relative non-re?conciliee?',
            'unreconciled relative uncertainty',
            'sigma in %',
            ANALYSIS_VALUE_IN_SIGMA_PRCT],
        ANALYSIS_NB_SIGMAS: [
            'eloignement de la valeur re?conciliee? par rapport a? la valeur non-re?conciliee?',
            'distance of the reconciled value compared to the unreconciled value',
            'ecart entree/sortie exprime en nombre d\'ecart-type',
            ANALYSIS_NB_SIGMAS],
        ANALYSIS_AI: ['ai', ANALYSIS_AI],
        ANALYSIS_CLASSIF: ['type de variable', 'variable type', ANALYSIS_CLASSIF]
    },
    UNCERTAINTY_SHEET: {
        RESULTS_ORIGIN: ['origine?', RESULTS_ORIGIN],
        RESULTS_DESTINATION: ['destination', 'target', RESULTS_DESTINATION]
    },
    CONVERSIONS_SHEET: {
        CONVERSIONS_LOCATION: [
            'unite? locale',
            'local unit',
            'locale?',
            'localites?',
            'locations?',
            CONVERSIONS_LOCATION],
        CONVERSIONS_PRODUCT:  ['produits?', 'products?', CONVERSIONS_PRODUCT],
        CONVERSIONS_NATURAL_UNIT: ['unite naturelle', 'natural unit', CONVERSIONS_NATURAL_UNIT],
        CONVERSIONS_FACTOR: [
            'facteur de conversion.*',
            'conversion factor.*',
            'unite equivalente ?/ ?unite naturelle',
            'equivalent unit ?/ ?natural unit'],
        CONVERSIONS_FACTOR_INV: [
            'inverse facteur de conversion.*',
            'inversed conversion factor.*',
            'unite naturelle ?/ ?unite equivalente',
            'natural unit ?/ ?equivalent unit'],
        CONVERSIONS_COMMENTARY: ['commentaires?', 'commentarys?', CONVERSIONS_COMMENTARY]
    }
}


# Helping comments which will be displayed for each columns of Output Excel file.
DICT_OF_COMMENTS = {
    TAG_SHEET: {
        TAG_NAME: ['Cette colonne permet de lister les différents noms de groupe d\'étiquettes\
                   présents pour présenter de façon différente les données sur les diagrammes de Sankey.'],
        TAG_TYPE: ['Il existe trois types d\'étiquettes qui peuvent êter utilisées: \n\
                   Etiquette_dimension: Cette étiquette permet de rajouter des dimensions\
                   de temps ou d\'espace pour avoir plusieurs représentations (spatiales ou temporelles)\
                   de la filière.\n Pour donner un exemple, plusieurs années peuvent être renseignées dans\
                   le même fichier pour toutes les données, et ces données sur la même filière pourront\
                   être affichées indépendamment pour chaque année. \n Etiquette_noeud: Cette étiquette\
                   permet de rajouter une information sur des noeuds pour, par la suite, pouvoir les filtrer\
                   sur le diagramme de Sankey. Il pourra ainsi être choisi de n\'afficher que certaines\
                   sous-parties de la filière étudiée. \n Etiquette_flux: Cette étiquette permet de rajouter\
                   une information sur les flux pour pouvoir afficher des informations sur les flux et sur\
                   les données utilisées grâce à des codes couleurs différents. Un exemple serait le degré \
                   d\'incertitude de la donnée, ou encore les sources utilisées.'],
        TAG_TAGS: ['Cette colonne rassemble toutes les étiquettes appartenant aux groupes\
                   d\'étiquette définis en colonne A. \n Il faut lister tous les noms d\'étiquettes\
                   en les séparant un double point. \n Exemple: nom1:nom2:nom3.'],
        TAG_IS_PALETTE: ['Cette colonne permet de déterminer quelle palette de couleur\
                         (étant associée à un groupe d\'étiquette) sera pris en compte pour\
                         la représentation graphique sous forme de diagramme de Sankey. \n\
                         Pour ce faire, il faut placer un 1 sur la ligne du groupe d\'étiquette\
                         choisi comme référence.'],
        TAG_COLORMAP: ['Palette de couleur'],
        TAG_COLOR: ['Couleurs']
    },
    NODES_SHEET: {
        NODES_LEVEL: ['Niveau', 'Level'],
        NODES_NODE: ['Noeuds'],
        NODES_MAT_BALANCE: ['Contraintes de conservation de la masse'],
        NODES_SANKEY: ['Affichage sur le diagramme de Sankey'],
        NODES_COLOR: ['Couleur'],
        NODES_DEFINITIONS: ['Définitions']
    },
    PRODUCTS_SHEET: {
        NODES_LEVEL: ['Le niveau d\'agrégation rend compte du détail d\'un produit. Il faut le lire\
                      comme étant, pour un niveau d’agrégation donné d\'un produit n, la somme de\
                      ses produits désagrégés au niveau n+1.'],
        NODES_NODE: ['Liste des produits présents dans l\'analyse de flux matière. \n Ceux-ci doivent\
                     êtreprésentés dans l\'ordre logique d\'agrégation des produits et doivent donc être\
                     compatibles avec les niveaux d\'agrégation donnés sur la colonne de gauche.'],
        NODES_MAT_BALANCE: ['Cette colonne permet d\'indiquer si la conservation de la masse doit être\
                            appliquée aux données concernant le produit considéré lors de la réconciliation.\
                            \n Si c\'est le cas, un 1 doit être renseigné sur la ligne du produit.'],
        NODES_SANKEY: ['Affichage sur le diagramme de Sankey'],
        NODES_COLOR: ['Couleur'],
        NODES_DEFINITIONS: ['Définitions']
    },
    SECTORS_SHEET: {
        NODES_LEVEL: ['Le niveau d\'agrégation rend compte du détail d\'un secteur.\
                      Il faut le lire comme étant, pour un niveau d\'agrégation donné d\'un\
                      secteur n, la somme de ses secteurs désagrégés au niveau n+1.'],
        NODES_NODE: ['Liste des secteurs présents dans l\'analyse de flux matière.\
                     \n Ceux-ci doivent être conformes aux niveaux d\'agrégation donnés sur la colonne de gauche.'],
        NODES_MAT_BALANCE: ['Cette colonne permet d\'indiquer si la conservation de\
                            la masse doit être appliquée aux données concernant le secteur lors de la\
                            réconciliation.\n Si c\'est le cas, un 1 doit être renseigné sur la ligne de ce secteur.'],
        NODES_SANKEY: ['Affichage sur le diagramme de Sankey'],
        NODES_COLOR: ['Couleur'],
        NODES_DEFINITIONS: ['Définitions']
    },
    EXCHANGES_SHEET: {
        NODES_LEVEL: ['Le niveau d\'agrégation rend compte du détail d\'un échange.\
                      Il faut le lire comme étant, pour un niveau d’agrégation donné d\'un\
                      échange n, la somme de ses échanges désagrégés au niveau n+1.'],
        NODES_NODE: ['Liste des échanges présents dans l\'analyse de flux matière. \n\
                     Ceux-ci doivent être conformes aux niveaux d\'agrégation donnés sur la colonne de gauche.'],
        NODES_SANKEY: ['Affichage sur le diagramme de Sankey'],
        NODES_COLOR: ['Couleur'],
        NODES_DEFINITIONS: ['Définitions']
    },
    DATA_SHEET: {
        DATA_ORIGIN: ['Origine du flux.\n\nDonnée obligatoire pour réaliser l\'AFM.'],
        DATA_DESTINATION: ['Destination du flux.\n\nDonnée obligatoire pour réaliser l\'AFM.'],
        DATA_VALUE: ['Valeur du flux dans l\'unité de référence de l\'AFM.\n\nDonnée\
                     obligatoire pour réaliser l\'AFM.'],
        DATA_QUANTITY: ['La quantité naturelle fait référence à la quantité exprimée\
                        dans l\'unité utilisée dans la source de la donnée.'],
        DATA_NATURAL_UNIT: ['La quantité naturelle fait référence à la quantité exprimée\
                            dans l\'unité utilisée dans la source de la donnée.'],
        DATA_FACTOR: ['Facteur de conversion'],
        DATA_UNCERT: ['L\'incertitude porte sur les données. Elle est soit renseignée par\
                      la source et recopiée ici, soit renseignée de manière arbitraire par\
                      la personne faisant l\'AFM en fonction de la confiance dans les\
                      données présentées par la source, selon la méthodologie décrite\
                      dans la première feuille de cet Excel.'],
        DATA_SOURCE: ['La source peut ici faire référence à une source de données externe\
                      au fichier Excel, ou à des données recopiées dans\
                      celui-ci dans les pages annexes à la fin de l\'excel.'],
        DATA_HYPOTHESIS: ['La colonne hypothèse permet de renseinger les hypothèses prises\
                          pour obtenir la donnée en unité de référence.']
    },
    MIN_MAX_SHEET: {
        MIN_MAX_ORIGIN: ['Origine du flux.\n\nDonnée obligatoire pour réaliser l\'AFM.'],
        MIN_MAX_DESTINATION: ['Destination du flux.\n\nDonnée obligatoire pour réaliser l\'AFM.'],
        MIN_MAX_MIN: ['Borne inférieure de la valeur possible du flux en unité de référence de l\'AFM. \n\
                      Donnée obligatoire pour réaliser l\'AFM.'],
        MIN_MAX_MAX: ['Borne supérieur de la valeur possible du flux en unité de référence de l\'AFM. \n\
                      Donnée obligatoire pour réaliser l\'AFM.'],
        MIN_MAX_MIN_QUANTITY: ['Borne inférieure de la valeur possible du flux en unité\
                               naturelle de la source de données.'],
        MIN_MAX_MAX_QUANTITY: ['Borne supérieur de la valeur possible du flux en unité\
                               naturelle de la source de données.'],
        MIN_MAX_NATURAL_UNIT: ['L\'unité naturelle fait référence à l\'unité utilisée dans la source de données.'],
        MIN_MAX_FACTOR: ['Le facteur de conversion (Fc) est le facteur permettant de passer de l\'unité\
                         naturelle (Un) à l\'unité de référence (Ur) grâce à l\'équation: \n Ur = Fc * Un'],
        MIN_MAX_SOURCE: ['La source peut ici faire référence à une source de données externe au fichier\
                         Excel, ou à des données recopiées dans celui-ci dans les pages annexes à la fin de l\'excel.'],
        MIN_MAX_HYPOTHESIS: ['La colonne hypothèse permet de renseinger les hypothèses prises pour obtenir\
                         la donnée en unité de référence.']
    },
    CONSTRAINTS_SHEET: {
        CONSTRAINT_ID: ['L\'identifiant permet de lier les flux appartenant à la même relation contrainte.'],
        CONSTRAINT_ORIGIN: ['Origine du flux. \n Donnée obligatoire pour réaliser l\'AFM'],
        CONSTRAINT_DESTINATION: ['Destination du flux. \n Donnée obligatoire pour réaliser l\'AFM'],
        CONSTRAINT_EQ: ['Cette colonne permet d\'insérer une contrainte d\'égalité sur les flux ayant le\
                        même identifiant. \n Pour donner un exemple, si il y a deux flux de valeur X et Y étant\
                        lié par une contrainte a*X = b*Y, eq = 0 doit se lire comme étant: \n a*X - b*Y = 0 \n\
                        Il faut donc renseigner a pour le flux de valeur X et -b pour le flux de valeur Y dans la\
                        colonne D.\n Donnée obligatoire pour réaliser l\'AFM si la contrainte est\
                        une contrainte d\'égalité.'],
        CONSTRAINT_INEQ_INF: ['Cette colonne permet d\'insérer une contrainte d\'inégalité sur les flux \
                              ayant le même identifiant. \n Pour donner un exemple, si il y a deux flux \
                              de valeur X et Y étant lié par une contrainte a*X <= b*Y, eq  <= 0 doit se\
                              lire comme étant: \n a*X - b*Y <= 0 \n Il faut donc renseigner a pour le flux\
                              de valeur X et -b pour le flux de valeur Y dans la colonne F. \n\
                              Donnée obligatoire pour réaliser l\'AFM si la contrainte est une\
                                contrainte d\'inégalité haute.'],
        CONSTRAINT_INEQ_SUP: ['Cette colonne permet d\'insérer une contrainte d\'inégalité sur les flux \
                              ayant le même identifiant. \n Pour donner un exemple, si il y a deux flux \
                              de valeur X et Y étant lié par une contrainte a*X >= b*Y, eq >= 0 doit se \
                              lire comme étant: \n a*X - b*Y >= 0 \n Il faut donc renseigner a pour le flux\
                              de valeur X et -b pour le flux de valeur Y dans la colonne E. \n Donnée obligatoire\
                              pour réaliser l\'AFM si la contrainte est une contrainte d\'inégalité basse.'],
        CONSTRAINT_TRADUCTION: ['Traduction'],
        CONSTRAINT_SOURCE: ['La source peut ici faire référence à une source de données externe au fichier \
                            Excel, ou à des données recopiées dans celui-ci dans les pages annexes\
                            à la fin de l\'excel.'],
        CONSTRAINT_HYPOTHESIS: ['La colonne hypothèse permet de renseinger les hypothèses prises pour obtenir \
                                la donnée en unité de référence.']
    },
    RESULTS_SHEET: {
        RESULTS_ORIGIN: ['Origine'],
        RESULTS_DESTINATION: ['Destination'],
        RESULTS_VALUE: ['Valeur de sortie du modèle'],
        RESULTS_FREE_MIN: ['Borne inférieure des variables libres'],
        RESULTS_FREE_MAX: ['Borne supérieure des variables libres']
    },
    ANALYSIS_SHEET: {
        RESULTS_ORIGIN: ['Origine'],
        RESULTS_DESTINATION: ['Destination'],
        RESULTS_VALUE: ['Valeur de sortie du modèle'],
        RESULTS_FREE_MIN: ['Borne inférieure des variables libres'],
        RESULTS_FREE_MAX: ['Borne supérieure des variables libres'],
        ANALYSIS_VALUE_IN: ['Valeur d\'entrée'],
        ANALYSIS_VALUE_MIN_IN: ['Minimum d\'entrée'],
        ANALYSIS_VALUE_MAX_IN: ['Maximum d\'entrée'],
        ANALYSIS_VALUE_IN_SIGMA: ['Incertitude d\'entrée'],
        ANALYSIS_NB_SIGMAS: ['Ecart entrée/sortie exprimé en nombre d\'écart-type'],
        ANALYSIS_CLASSIF: ['Type de variable']
    },
    CONVERSIONS_SHEET: {
        CONVERSIONS_LOCATION: ['Locale'],
        CONVERSIONS_PRODUCT: ['Liste des produits sur lesquelles s\'applique les conversions d`unité'],
        CONVERSIONS_COMMENTARY: ['Commentaire éventuel sur le noeud et sa conversion'],
        CONVERSIONS_NATURAL_UNIT: ['Unité naturelle pour les produits listés'],
        CONVERSIONS_FACTOR: ['Facteur de conversion depuis l\'unité naturelle vers l\'unité équivalente au diagramme'],
        CONVERSIONS_FACTOR_INV: [
            'Facteur de conversion depuis l\'unité equivalente vers l\'unité naturelle au diagramme'],
    }
}
