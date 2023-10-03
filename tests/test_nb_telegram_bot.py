# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import nb_telegram_bot
from hypothesis import given, strategies as st

# TODO: replace st.nothing() with appropriate strategies


#@given(
    #statement=st.nothing(),
    #params=st.nothing(),
    #orig=st.nothing(),
    #hide_parameters=st.booleans(),
    #connection_invalidated=st.booleans(),
    #code=st.none(),
    #ismulti=st.none(),
#)
#def test_fuzz_ProgrammingError(
    #statement, params, orig, hide_parameters, connection_invalidated, code, ismulti
#) -> None:
    #nb_telegram_bot.ProgrammingError(
        #statement=statement,
        #params=params,
        #orig=orig,
        #hide_parameters=hide_parameters,
        #connection_invalidated=connection_invalidated,
        #code=code,
        #ismulti=ismulti,
    #)


@given(bottoken=st.text(), spoon_token=st.text(), sql_auth=st.builds(dict))
def test_fuzz_create_bot(bottoken: str, spoon_token: str, sql_auth: dict) -> None:
    nb_telegram_bot.create_bot(
        bottoken=bottoken, spoon_token=spoon_token, sql_auth=sql_auth
    )
