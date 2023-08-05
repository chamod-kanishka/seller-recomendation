# -----Imports-----
import pandas as pd

from Recommendation import SellerRecommendationSystem

# -----Loading initial dataset-----
df = pd.read_csv("./data/seller_rank.csv")

# -----Extract only unique combinations-----
unique_df = df.groupby(['user_id', 'seller_id', 'review_product', 'review_delivery', 'review_communication']).size().reset_index().rename(columns={0: 'count'})

# -----Trainig algorithm-----
def train_recommendation_system():
    # Count of users, sellers, and episodes
    num_users = unique_df['user_id'].nunique() + 1
    num_sellers = unique_df['seller_id'].nunique()
    num_episodes = unique_df.count()[0]

    # Create instance for seller recommendation system
    system = SellerRecommendationSystem(num_users, num_sellers)

    for episode in range(num_episodes):
        # Simulate interactions
        for user_id in range(1, num_users):
            # Get recommended seller
            recommended_seller = system.recommend(user_id)
            # Get rewards by using get_reward function
            reward_product, reward_delivery, reward_communication = system.get_reward(user_id, recommended_seller)

            # If any of the rewards is greater than zero, the user has interacted with the seller
            if reward_product > 0 or reward_delivery > 0 or reward_communication > 0:
                # Update the recommendation system with acquired values
                system.update(user_id, recommended_seller, reward_product, reward_delivery, reward_communication)

    return True
