import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('Agg')
# Load the JSON data

def makegraph(data_path,output_path):
    with open(data_path, 'r') as f:
        data = json.load(f)

    # Extract list of unique models and questions
    models = list(set(entry['model'] for entry in data))
    questions = list(set(entry['question'] for entry in data))

    # Create a DataFrame for easier plotting with seaborn
    rows = []
    for entry in data:
        rows.append({
            'model': entry['model'],
            'question': entry['question'],
            'jailbreakSuccess': int(entry['jailbreakSucess'])
        })

    df = pd.DataFrame(rows)

    # Pivot the data to get models as rows, questions as columns
    pivot_table = df.pivot_table(index='question', columns='model', values='jailbreakSuccess', fill_value=0).T

    # Plot using seaborn
    plt.figure(figsize=(12, 10))
    # Scale from 0 (red) to 1 (blue)
    ax = sns.heatmap(pivot_table, annot=True, fmt='g', cmap='coolwarm_r', linewidths=.5, vmin=0, vmax=1)

    # Add color bar with custom ticks
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks([0, 1])
    colorbar.set_ticklabels(['Fail', 'Success'])

    # Compressing question labels to show only first few characters
    compressed_questions = [q[:10] + '...' if len(q) > 10 else q for q in questions]
    ax.set_xticklabels(compressed_questions, rotation=90)
    ax.set_yticklabels(models)

    plt.title('Jailbreak Success Matrix')
    plt.xlabel('Questions')
    plt.ylabel('Models')

    # Save the figure as an image file
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

    print(f'image saved at {output_path}')

if __name__ == "__main__":
    makegraph(data_path = './result_DUDE.json',output_path = './result_DUDE.png')
    makegraph(data_path = './result_DAN.json',output_path = './result_DAN.png')
    makegraph(data_path = './result_TOM.json',output_path = './result_TOM.png')