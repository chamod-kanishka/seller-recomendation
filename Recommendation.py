# -----Imports-----
import numpy as np
import tensorflow as tf
import pandas as pd

# -----Loading initial dataset-----
df = pd.read_csv("./data/seller_rank.csv")

# -----Extract only unique combinations-----
unique_df = df.groupby(['user_id', 'seller_id', 'review_product', 'review_delivery', 'review_communication']).size().reset_index().rename(columns={0: 'count'})

# -----Define the agent-----
class RecommenderAgent:
    # Constructor
    def __init__(self, num_sellers, learning_rate=0.001, discount_factor=0.95, epsilon=1.0, epsilon_decay=0.99):
        self.num_sellers = num_sellers
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

        self.q_values = np.zeros(num_sellers)
        self.model = self.build_model()

    # Function to build the neural network model
    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(self.num_sellers,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.num_sellers, activation='softmax')
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
                      loss=tf.keras.losses.MeanSquaredError())
        return model

    # Function select an action
    def choose_action(self):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.num_sellers)
        return np.argmax(self.q_values)

    # Function to update Q values
    def update(self, user_id, action, rewards, next_state):
        q_value = self.q_values[action]
        next_max_q = np.max(self.q_values[next_state])

        weight_product = 1.0
        weight_delivery = 0.9
        weight_communication = 0.8

        total_reward = (rewards[0]*weight_product)+ (rewards[1]*weight_delivery)+ (rewards[2]*weight_communication)
        # total_reward = sum(rewards)  # Sum of all rewards
        updated_q = q_value + self.learning_rate * (total_reward + self.discount_factor * next_max_q - q_value)
        self.q_values[action] = updated_q

        if self.epsilon > 0.01:
            self.epsilon *= self.epsilon_decay

# -----Define the overall recommendation system-----
# States -> Users, Actions -> Sellers, Rewards -> User Reviews
class SellerRecommendationSystem:
    # Constructor
    def __init__(self, num_users, num_sellers):
        self.num_users = num_users
        self.num_sellers = num_sellers
        self.user_preferences = [[] for _ in range(num_users)]
        self.recommender_agents = [RecommenderAgent(num_sellers) for _ in range(num_users)]
        self.initiat_data = unique_df

    # Function to recommend sellers
    def recommend(self, user_id):
        agent = self.recommender_agents[user_id]
        action = agent.choose_action()
        return action

    # Function to update the agent
    def update(self, user_id, seller_id, reward_product, reward_delivery, reward_communication):
        agent = self.recommender_agents[user_id]
        action = seller_id
        rewards = [reward_product, reward_delivery, reward_communication]
        agent.update(user_id, action, rewards, next_state=None)
        self.user_preferences[user_id].append([reward_product, reward_delivery, reward_communication])

    # Function to get rewards from the initial dataset
    def get_reward(self, user_id, recommended_seller):
        # Retrieve user's review for the recommended seller
        user_preference = self.initiat_data.loc[(self.initiat_data["user_id"] == user_id) & (self.initiat_data["seller_id"] == recommended_seller)]

        # Create rewards based on review_product, review_delivery, and review_communication values
        review_product = user_preference["review_product"].tolist()
        review_delivery = user_preference["review_delivery"].tolist()
        review_communication = user_preference["review_communication"].tolist()

        reward_product = 0.0
        reward_delivery = 0.0
        reward_communication = 0.0

        if len(review_product) > 0:
            if review_product[0] == "good":
                reward_product = 1.0
            elif review_product[0] == "bad":
                reward_product = -1.0

        if len(review_delivery) > 0:
            if review_delivery[0] == "good":
                reward_delivery = 1.0
            elif review_delivery[0] == "bad":
                reward_delivery = -1.0

        if len(review_communication) > 0:
            if review_communication[0] == "good":
                reward_communication = 1.0
            elif review_communication[0] == "bad":
                reward_communication = -1.0

        return reward_product, reward_delivery, reward_communication                    
