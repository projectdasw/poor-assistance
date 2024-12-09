from os import environ

SESSION_CONFIGS = [
    dict(
        display_name='Poor Assistance Experiment (Beta)',
        name='poor_assistance_experiment',
        app_sequence=[
            'welcome_instructions',
            'risky_option_price',
            'risky_option_allocation',
            'cognitive_task',
            'asian_handicap',
            'survey',
            'pay_random'
        ],
        num_demo_participants=1
    ),
    dict(
        display_name='Risky Option Price',
        name='risky_option_price',
        app_sequence=['risky_option_price'],
        num_demo_participants=1
    ),
    dict(
        display_name='Risky Option Allocation',
        name='risky_option_allocation',
        app_sequence=['risky_option_allocation'],
        num_demo_participants=1
    ),
    dict(
        display_name='Cognitive Task',
        name='cognitive_task',
        app_sequence=['cognitive_task'],
        num_demo_participants=1
    ),
    dict(
        display_name='ASIAN Handicap',
        name='asian_handicap',
        app_sequence=['asian_handicap'],
        num_demo_participants=1
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

SESSION_FIELDS = [
    'completions_by_treatment',
    'past_groups',
    'matrices',
    'wait_for_ids',
    'arrived_ids',
]

PARTICIPANT_FIELDS = [
    'get_endowment',
    'get_payment',
    'offer_accepted',
    'still_interested',
    'board',
    'dynamic_endowment',
    'app_payoffs',
    'app_row',
    'expiry',
    'finished_rounds',
    'language',
    'num_rounds',
    'partner_history',
    'past_group_id',
    'progress',
    'quiz_num_correct',
    'selected_round',
    'task_rounds',
    'time_pressure',
    'wait_page_arrival',
    'umr_list',
    'iw_lists',
    'sw_lists',
    'endowment_lists',
    'iw_type',
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False

DEBUG=True
ADMIN_USERNAME = 'admin'
# for security, best to set admin passwordInput in an environment variable
ADMIN_PASSWORD = 'admin'
AUTH_LEVEL= environ.get('OTREE_AUTH_LEVEL')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5123142091007'
