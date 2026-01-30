import streamlit as st
from phevaluator import evaluate_cards
import random
import itertools
from collections import defaultdict

st.set_page_config(
    page_title="Texas Hold'em Equity Calculator",
    page_icon="♠️",
    layout="wide"
)

suits = {'d': '♦', 's': '♠', 'c': '♣', 'h': '♥'}

ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

all_cards = [r + s for r in ranks for s in suits.keys()]

card_display = {card: f"{r}{suits[s]}" for r in ranks for s in suits.keys() for card in [r + s]}


def get_card_display(card):
    return card_display.get(card, card)


def simulate_montecarlo(hand, table, num_opponents=1, num_simulations=1000):

    deck = all_cards.copy()

    known_cards = hand + table
    for card in known_cards:
        if card in deck:
            deck.remove(card)

    win_count = 0
    lose_count = 0
    tie_count = 0

    for _ in range(num_simulations):
        random.shuffle(deck)

        sim_deck = deck.copy()

        opponents_hands = []
        for _ in range(num_opponents):
            opp_hand = [sim_deck.pop(), sim_deck.pop()]
            opponents_hands.append(opp_hand)

        community_cards = table.copy()
        while len(community_cards) < 5:
            community_cards.append(sim_deck.pop())

        my_rank = evaluate_cards(*(hand + community_cards))

        result = 0
        for opp_hand in opponents_hands:
            opp_rank = evaluate_cards(*(opp_hand + community_cards))

            if opp_rank < my_rank:
                result = 1
                break
            elif opp_rank == my_rank:
                result = 2

        if result == 0:
            win_count += 1
        elif result == 1:
            lose_count += 1
        else:
            tie_count += 1

    return win_count / num_simulations, lose_count / num_simulations, tie_count / num_simulations


def calculate_exact_equity(hand, table, num_opponents=1):
    known_cards = hand + table
    remaining_cards = [card for card in all_cards if card not in known_cards]

    if len(table) == 5:
        win_count = 0
        total_count = 0

        for opp_cards in itertools.combinations(remaining_cards, 2 * num_opponents):
            if num_opponents == 1:
                my_rank = evaluate_cards(*(hand + table))
                opp_rank = evaluate_cards(*(list(opp_cards) + table))

                if my_rank < opp_rank:
                    win_count += 1
                elif my_rank == opp_rank:
                    win_count += 0.5

                total_count += 1

        if total_count > 0:
            win_prob = win_count / total_count
            return win_prob, 1 - win_prob, 0.0

    return None, None, None


def get_hand_strength(hand, table):
    if len(table) < 3:  # Need at least flop to evaluate hand
        return "Waiting for flop..."

    try:
        all_cards_list = hand + table
        rank = evaluate_cards(*all_cards_list)

        if rank <= 1:
            return "Royal Flush! 🎉"
        elif rank <= 10:
            return "Straight Flush!"
        elif rank <= 166:
            return "Four of a Kind"
        elif rank <= 322:
            return "Full House"
        elif rank <= 1599:
            return "Flush"
        elif rank <= 1609:
            return "Straight"
        elif rank <= 2467:
            return "Three of a Kind"
        elif rank <= 3325:
            return "Two Pair"
        elif rank <= 6185:
            return "One Pair"
        else:
            return "High Card"
    except:
        return "Evaluating..."


st.title("♠️ Texas Hold'em Equity Calculator")
st.markdown("---")

col1, col2 = st.columns([2, 3])

with col1:
    st.header("🃏 Input Cards")

    st.subheader("1. Select Your Hole Cards")

    hand_col1, hand_col2 = st.columns(2)

    with hand_col1:
        hand1_rank = st.selectbox("First Card Rank", ranks, index=0, key="hand1_rank")
        hand1_suit = st.selectbox("First Card Suit", list(suits.keys()),
                                  format_func=lambda x: suits[x], index=1, key="hand1_suit")

    with hand_col2:
        hand2_rank = st.selectbox("Second Card Rank", ranks, index=11, key="hand2_rank")
        hand2_suit = st.selectbox("Second Card Suit", list(suits.keys()),
                                  format_func=lambda x: suits[x], index=3, key="hand2_suit")

    hand = [hand1_rank + hand1_suit, hand2_rank + hand2_suit]

    st.markdown(f"**Your Hand:** {get_card_display(hand[0])}  {get_card_display(hand[1])}")

    st.subheader("2. Select Community Cards")

    flop_cols = st.columns(3)
    flop_cards = []

    for i in range(3):
        with flop_cols[i]:
            enabled = st.checkbox(f"Flop {i + 1}", value=(i < 3), key=f"flop{i}_enabled")
            if enabled:
                rank = st.selectbox(f"Rank", ranks, index=i, key=f"flop{i}_rank")
                suit = st.selectbox(f"Suit", list(suits.keys()),
                                    format_func=lambda x: suits[x], index=i, key=f"flop{i}_suit")
                flop_cards.append(rank + suit)
            else:
                flop_cards.append(None)

    turn_col, river_col = st.columns(2)

    with turn_col:
        turn_enabled = st.checkbox("Turn", value=False, key="turn_enabled")
        if turn_enabled:
            turn_rank = st.selectbox("Rank", ranks, index=3, key="turn_rank")
            turn_suit = st.selectbox("Suit", list(suits.keys()),
                                     format_func=lambda x: suits[x], index=0, key="turn_suit")
            turn_card = turn_rank + turn_suit
        else:
            turn_card = None

    with river_col:
        river_enabled = st.checkbox("River", value=False, key="river_enabled")
        if river_enabled:
            river_rank = st.selectbox("Rank", ranks, index=4, key="river_rank")
            river_suit = st.selectbox("Suit", list(suits.keys()),
                                      format_func=lambda x: suits[x], index=1, key="river_suit")
            river_card = river_rank + river_suit
        else:
            river_card = None

    table = [card for card in flop_cards if card is not None]
    if turn_card:
        table.append(turn_card)
    if river_card:
        table.append(river_card)

    if table:
        table_display = "  ".join([get_card_display(card) for card in table])
        st.markdown(f"**Community Cards:** {table_display}")
    else:
        st.markdown("**Community Cards:** None")

    st.subheader("3. Game Settings")

    opponents = st.slider("Number of Opponents", 1, 9, 1, 1)
    simulations = st.slider("Number of Simulations", 100, 50000, 10000, 100)

    if st.button("🚀 Calculate Equity", type="primary", use_container_width=True):
        all_used = hand + table
        if len(set(all_used)) != len(all_used):
            st.error("Error: Duplicate cards detected!")
        else:
            with st.spinner(f"Calculating... (running {simulations:,} simulations)"):
                win_p, lose_p, tie_p = simulate_montecarlo(hand, table, opponents, simulations)

                st.session_state['results'] = {
                    'win': win_p,
                    'lose': lose_p,
                    'tie': tie_p,
                    'hand': hand.copy(),
                    'table': table.copy(),
                    'opponents': opponents,
                    'simulations': simulations
                }

with col2:
    st.header("📊 Equity Analysis")

    if len(table) >= 3:
        strength = get_hand_strength(hand, table)
        st.info(f"**Hand Strength:** {strength}")

    if 'results' in st.session_state:
        results = st.session_state['results']

        current_input = hand + table
        saved_input = results['hand'] + results['table']

        if current_input != saved_input or opponents != results['opponents']:
            st.warning("⚠️ Settings have changed. Please recalculate.")
        else:
            win_p, lose_p, tie_p = results['win'], results['lose'], results['tie']

            st.subheader("Equity Distribution")

            st.progress(win_p, text=f"Win: {win_p * 100:.2f}%")
            st.progress(lose_p, text=f"Lose: {lose_p * 100:.2f}%")
            st.progress(tie_p, text=f"Tie: {tie_p * 100:.2f}%")

            chart_data = {
                'Outcome': ['Win', 'Lose', 'Tie'],
                'Probability': [win_p, lose_p, tie_p]
            }

            import pandas as pd
            import plotly.express as px

            df = pd.DataFrame(chart_data)
            fig = px.pie(df, values='Probability', names='Outcome',
                         color='Outcome',
                         color_discrete_map={'Win': 'green', 'Lose': 'red', 'Tie': 'blue'},
                         hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Detailed Metrics")

            info_cols = st.columns(3)
            with info_cols[0]:
                st.metric("Win Rate", f"{win_p * 100:.2f}%")
            with info_cols[1]:
                st.metric("Lose Rate", f"{lose_p * 100:.2f}%")
            with info_cols[2]:
                st.metric("Tie Rate", f"{tie_p * 100:.2f}%")

            if len(table) == 5:
                st.subheader("Hand Type Analysis")

                deck = all_cards.copy()
                known_cards = hand + table
                for card in known_cards:
                    if card in deck:
                        deck.remove(card)

                hand_types = defaultdict(int)
                total_trials = min(1000, len(deck) * 10)

                for _ in range(total_trials):
                    random.shuffle(deck)
                    sim_deck = deck.copy()

                    opp_hand = [sim_deck.pop(), sim_deck.pop()]
                    all_cards_list = opp_hand + table
                    rank = evaluate_cards(*all_cards_list)

                    if rank <= 1:
                        hand_types['Royal Flush'] += 1
                    elif rank <= 10:
                        hand_types['Straight Flush'] += 1
                    elif rank <= 166:
                        hand_types['Four of a Kind'] += 1
                    elif rank <= 322:
                        hand_types['Full House'] += 1
                    elif rank <= 1599:
                        hand_types['Flush'] += 1
                    elif rank <= 1609:
                        hand_types['Straight'] += 1
                    elif rank <= 2467:
                        hand_types['Three of a Kind'] += 1
                    elif rank <= 3325:
                        hand_types['Two Pair'] += 1
                    elif rank <= 6185:
                        hand_types['One Pair'] += 1
                    else:
                        hand_types['High Card'] += 1

                for hand_type in ['Royal Flush', 'Straight Flush', 'Four of a Kind',
                                  'Full House', 'Flush', 'Straight', 'Three of a Kind',
                                  'Two Pair', 'One Pair', 'High Card']:
                    if hand_type in hand_types:
                        prob = hand_types[hand_type] / total_trials * 100
                        st.text(f"{hand_type}: {prob:.1f}%")
    else:
        st.info("👈 Please set your cards and click 'Calculate Equity'")

        st.markdown("""
        ### 💡 How to Use:
        1. **Select your two hole cards** on the left
        2. **Choose community cards** (flop, turn, river)
        3. **Set number of opponents and simulations**
        4. **Click the 'Calculate Equity' button**

        ### 🎯 Tips:
        - Pre-flop equity: Don't select any community cards
        - Post-flop equity: Select 3 flop cards
        - Post-turn equity: Select 4 community cards
        - Post-river equity: Select all 5 community cards
        """)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <small>Texas Hold'em Equity Calculator | Powered by phevaluator library | Simulation results for reference only</small>
    </div>
    """,
    unsafe_allow_html=True
)