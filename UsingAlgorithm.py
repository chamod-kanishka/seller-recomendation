# -----Imports-----
from Recommendation import SellerRecommendationSystem

# -----Get recommendation-----
def get_recommendation(user_count, seller_count, user_id_new):
    # Create new instance for seller recommendation system
    system_new = SellerRecommendationSystem(int(user_count), int(seller_count))

    recommended_seller = system_new.recommend(int(user_id_new))
    
    return recommended_seller

# -----Update recommendation system-----
def update_recommendation_system(user_count, seller_count, user_id, recommended_seller, reward_product, reward_delivery, reward_communication):
    # Convert user_count and seller_count to integers
    user_count = int(user_count)
    seller_count = int(seller_count)

    system_new = SellerRecommendationSystem(user_count, seller_count)
    system_new.update(int(user_id), int(recommended_seller), float(reward_product), float(reward_delivery), float(reward_communication))
    return True
