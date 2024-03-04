import numpy as np
from PIL import Image

def calculate_similarity(edge1, edge2):
    # Calculate the sum of squared differences for pixel intensity
    ssd = np.sum((edge1 - edge2) ** 2)
    # Combine the metrics
    return ssd  

def solve_shredded_image(image, shred_width=64):
    # Convert image to numpy array
    image_array = np.array(image)
    num_shreds = image.width // shred_width
    shreds = [image_array[:, i*shred_width:(i+1)*shred_width] for i in range(num_shreds)]
    
    order = [0]  # The first slice is correct
    used = {0}   # Mark the first slice as used
    
    while len(order) < num_shreds - 1:  # Stop before the last slice
        last_shred = shreds[order[-1]]
        best_match = None
        best_similarity = float('inf')
        
        for i, shred in enumerate(shreds):
            if i not in used:
                similarity = calculate_similarity(last_shred[:, -1], shred[:, 0])
                if similarity < best_similarity:
                    best_similarity = similarity
                    best_match = i
        
        order.append(best_match)
        used.add(best_match)
    
    # Identify the last slice by elimination
    last_slice = (set(range(num_shreds)) - used).pop()
    order.append(last_slice)

    # Now, specifically check if swapping the last two improves the overall similarity
    if len(order) > 2:  # Only makes sense if there are at least three slices
        second_to_last_slice = order[-2]
        last_slice = order[-1]
        
        # Compare the second-to-last slice to its new left neighbor and the last slice to the second-to-last's original left neighbor
        original_similarity = calculate_similarity(shreds[order[-3]][:, -1], shreds[second_to_last_slice][:, 0]) + \
                              calculate_similarity(shreds[second_to_last_slice][:, -1], shreds[last_slice][:, 0])
        swapped_similarity = calculate_similarity(shreds[order[-3]][:, -1], shreds[last_slice][:, 0]) + \
                             calculate_similarity(shreds[last_slice][:, -1], shreds[second_to_last_slice][:, 0])

        # If the similarity is improved by swapping, update the order
        if swapped_similarity < original_similarity:
            order[-2], order[-1] = order[-1], order[-2]  # Swap the slices

    return order  # Return the corrected order

# Main execution
image = Image.open("../Riddles/cv_easy_example/shredded.jpg")  # Ensure this image path is correct
solution_order = solve_shredded_image(image)
print(solution_order)  # This will print the final order of the pieces