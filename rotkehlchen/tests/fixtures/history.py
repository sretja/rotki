import pytest

from rotkehlchen.db.dbhandler import DBHandler
from rotkehlchen.exchanges.manager import ExchangeManager
from rotkehlchen.externalapis.cryptocompare import Cryptocompare
from rotkehlchen.history import PriceHistorian, TradesHistorian
from rotkehlchen.tests.utils.history import maybe_mock_historical_price_queries
from rotkehlchen.externalapis.coingecko import Coingecko


@pytest.fixture(name='cryptocompare')
def fixture_cryptocompare(data_dir, database):
    return Cryptocompare(data_directory=data_dir, database=database)


@pytest.fixture(scope='session', name='session_cryptocompare')
def fixture_session_cryptocompare(session_data_dir, session_database):
    return Cryptocompare(data_directory=session_data_dir, database=session_database)


@pytest.fixture(scope='session', name='session_coingecko')
def fixture_session_coingecko():
    return Coingecko()


@pytest.fixture
def price_historian(
        data_dir,
        inquirer,  # pylint: disable=unused-argument
        should_mock_price_queries,
        mocked_price_queries,
        cryptocompare,
        session_coingecko,
        default_mock_price_value,
):
    # Since this is a singleton and we want it initialized everytime the fixture
    # is called make sure its instance is always starting from scratch
    PriceHistorian._PriceHistorian__instance = None
    historian = PriceHistorian(
        data_directory=data_dir,
        cryptocompare=cryptocompare,
        coingecko=session_coingecko,
    )
    maybe_mock_historical_price_queries(
        historian=historian,
        should_mock_price_queries=should_mock_price_queries,
        mocked_price_queries=mocked_price_queries,
        default_mock_value=default_mock_price_value,
    )

    return historian


@pytest.fixture
def trades_historian(data_dir, function_scope_messages_aggregator, blockchain):
    database = DBHandler(
        user_data_dir=data_dir,
        password='123',
        msg_aggregator=function_scope_messages_aggregator,
        initial_settings=None,
    )
    exchange_manager = ExchangeManager(msg_aggregator=function_scope_messages_aggregator)
    historian = TradesHistorian(
        user_directory=data_dir,
        db=database,
        msg_aggregator=function_scope_messages_aggregator,
        exchange_manager=exchange_manager,
        chain_manager=blockchain,
    )
    return historian
