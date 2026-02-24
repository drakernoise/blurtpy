from blurtpy.blurt import Blurt
from blurtpy.comment import Comment
from blurtpy.amount import Amount
import json

def inspect_rewards():
    node = "https://rpc.beblurt.com"
    print(f"--- Conectando a {node} ---")
    stm = Blurt(node)
    
    # Obtener post trending para inspeccionar
    print("\n[DEBUG] Inspeccionando primer post de 'trending'...")
    trending = stm.get_discussions_by_trending({"limit": 1})
    if not trending:
        print("No se encontraron posts.")
        return

    post = trending[0]
    authorperm = f"@{post['author']}/{post['permlink']}"
    print(f"Post: {authorperm}")
    
    # 1. Comprobar keys crudas de la API
    print("\n[DEBUG] Raw API keys relevantes:")
    relevant_keys = ['pending_payout_value', 'total_payout_value', 'curator_payout_value', 'payout_SBD', 'payout_SP']
    for k in relevant_keys:
        print(f"  {k}: {post.get(k, 'N/A')}")

    # 2. Comprobar get_author_rewards()
    print("\n[DEBUG] Ejecutando Comment.get_author_rewards()...")
    try:
        c = Comment(post, blockchain_instance=stm)
        author_rewards = c.get_author_rewards()
        print("Resultados de get_author_rewards():")
        for k, v in author_rewards.items():
            print(f"  {k}: {v} ({type(v).__name__})")
            
        if 'payout_BP' in author_rewards:
            print("\n[SUCCESS] Se encontró la nueva key 'payout_BP'")
        else:
            print("\n[ERROR] NO se encontró 'payout_BP'")
            
    except Exception as e:
        print(f"CRASH en get_author_rewards: {type(e).__name__}: {str(e)}")

    # 3. Comprobar get_curation_rewards()
    print("\n[DEBUG] Ejecutando Comment.get_curation_rewards()...")
    try:
        curation_rewards = c.get_curation_rewards()
        print("Resultados de get_curation_rewards() (keys principales):")
        print(f"  pending_rewards: {curation_rewards.get('pending_rewards')}")
        print(f"  unclaimed_rewards: {curation_rewards.get('unclaimed_rewards')}")
        votos = curation_rewards.get('active_votes', {})
        print(f"  Número de votos procesados: {len(votos)}")
    except Exception as e:
        print(f"CRASH en get_curation_rewards: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    inspect_rewards()
