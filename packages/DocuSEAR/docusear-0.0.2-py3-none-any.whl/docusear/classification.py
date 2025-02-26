import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.backends.backend_pdf import PdfPages

import requests
import os

downloaded_images = set()




def pdf_output(*indices, inline=False):

    base_url = "https://github.com/VisualXAI/PyStorAI/blob/main/image"
    global num_images # debugging
    num_images = 0

    # Download requested images
    for i in indices:
        if i in downloaded_images:
            print(f"Image {i} already found.")
            num_images +=1
        else:
            url = f"{base_url}{i}.png?raw=true"

            response = requests.get(url)

            if response.status_code == 200:
                # Extract filename from URL
                file_name = f"image{i}.png"

                with open(file_name, 'wb') as f:
                    f.write(response.content)
                    print(f"Image {i} download successful.")

                # Rename file to remove "?raw=true"
                os.rename(file_name, f"image{i}.png")
                print(f"Image {i} filename changed.")

                # Update download index
                downloaded_images.add(i)
                # Count images downloaded
                num_images += 1
            else:
                print(f"Failed to download image {i}. Status code: {response.status_code}")
    
    global image_files # debugging
    image_files = [f"image{index}.png" for index in indices]


    # Determine storyboard layout
    global num_cols # debugging
    global num_rows # debugging
    if num_images <= 4:
        num_cols = num_images
    elif num_images <= 6:
        num_cols = 3
    elif num_images <= 8:
        num_cols = 4
    elif num_images == 9:
        num_cols = 3
    elif num_images <=12:
        num_cols = 4
    elif num_images <=15:
        num_cols = 5
    else:
        num_cols = 4

    num_rows = -(-num_images // num_cols)


    with PdfPages('output.pdf') as pdf:
        # plt.ioff() # Disable interactive mode

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols*2, num_rows*2))

        # Plot images in correct layout
        for i, file_name in enumerate(image_files):
          img = imread(file_name)
          ax = axes[i // num_cols, i % num_cols] if num_rows > 1 else axes[i % num_cols]
          ax.imshow(img)
          ax.axis('off')

        # Hide any remaining empty axes
        for i in range(num_images, num_rows * num_cols):
          axes.flatten()[i].axis('off')

        # Adjust layout and save to PDF
        plt.tight_layout()
        pdf.savefig()

        if inline: # Plot inline if inline=True
          plt.show()
        
        # plt.ion() # Re-enable interactive mode
        plt.close()



def show_all():

    base_url = "https://github.com/VisualXAI/PyStorAI/blob/main/image"
    captions_url = "https://raw.githubusercontent.com/VisualXAI/PyStorAI/main/captions.txt"
    max_images = 100 # Greater or equal to number of images
    global num_images # debugging
    num_images = 0

    # Download captions file
    response = requests.get(captions_url)
    with open('captions.txt', 'wb') as f:
        f.write(response.content)

    # Download all repository images
    for i in range(1, max_images + 1):
        url = f"{base_url}{i}.png?raw=true"

        response = requests.get(url)

        if response.status_code == 200:
            # Extract filename from URL
            file_name = f"image{i}.png"

            with open(file_name, 'wb') as f:
                f.write(response.content)
                print(f"Image {i} download successful.")

            # Rename file to remove "?raw=true"
            os.rename(file_name, f"image{i}.png")
            print(f"Image {i} filename changed.")

            # Count images downloaded
            num_images +=1
        else:
            print(f"Failed to download image {i}. Status code: {response.status_code}")
            break  # Stop downloading



    # Read captions from file
    captions = []
    with open('captions.txt', 'r') as captions_file:
        captions = captions_file.read().splitlines()

    global image_files # debugging
    image_files = [f"image{i}.png" for i in range(1, num_images + 1)]


    # Determine display layout
    global num_cols # debugging
    global num_rows # debugging
    num_cols = min(num_images, 4)
    num_rows = -(-num_images // num_cols)

    # Save images to PDF
    with PdfPages('output.pdf') as pdf:
        # plt.ioff()

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols*2, num_rows*2))

        # Plot images in correct layout
        for i, (file_name, caption) in enumerate(zip(image_files, captions)):
            img = imread(file_name)
            ax = axes[i // num_cols, i % num_cols] if num_rows > 1 else axes[i % num_cols]
            ax.imshow(img)

            # Add caption below image
            ax.text(0.5, -0.10, caption, transform=ax.transAxes, ha='center', va='center', fontsize=8, weight='bold')

            ax.axis('off')

        # Hide any remaining empty axes
        for i in range(num_images, num_rows * num_cols):
            axes.flatten()[i].axis('off')

        # Adjust layout and save to PDF
        plt.tight_layout()
        pdf.savefig()

        # plt.ion() # Re-enable interactive mode
        plt.close()

