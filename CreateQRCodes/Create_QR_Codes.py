
# Importing Libraries

#%%

import qrcode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pyfiglet


# Defining functions
## For full breakdown, see: Create QR Codes

test_data = "Astral Radiance PTCGL Code      TJX46MQBK6TLL      QJHCMTX6BMGCW      BVYV269PBBYWC      BQZRXD6HGXRC6      W46QNRNHYHCLR      N9CHL2N49BJY9      W9CXKM9JNVQVH      WT6R6NL9CM7KZ      9BK9B6NJBLKR2      9Z6M2N7VL4LN9      7G9KH7CBLH7ZB      6K6JT6VKBJN6V      6Y9X6W4MZLPP4      6JKJTVLYNMPMH      P9PZ729GXL9GQ      BKRKQXXLT2BK9      PMZYC2ZRBPM4W      PNHXW7Z2BN7DT      6JLMGRJR6MB9W      H7NQYH62JWBLD      BLHBGVCLMP9XJ      YN7BYKVLDWYNW      YPDNLTMG676VD      Q7NJHM9Z6YNTZ      QBXJYVP2NJW2K"

#%%

##########################
def fixing_PTCGL_codes(base_data):
    
    base_data_list = base_data.split('\n')
    # Splitting all the gaps between codes
    
    str_list = list(filter(None, base_data_list))
    # Removes empty rows if needed 
    
    str_list = [x.strip(' ') for x in str_list]
    # Deleting all spaces
    
    return str_list

#%%

########################
def create_QR(data_qr):
# Create simple QR code for packs
    
    qr = qrcode.QRCode(version=1, box_size=20, border=0)
    

    qr.add_data(data_qr)
    # Add the data to the QR code object
    
    qr.make(fit=True)
    # Make the QR code
    
    img = qr.make_image(fill_color="black", back_color="white")
    # Create an image from the QR code with a black fill color and white background
    
    return img

########################
def plot_multi_QR(images):
# Function to create the (2,5) array of QR codes from "images" input
    
    fig, axes = plt.subplots(2, 5, figsize=(20, 9))
    # Setting size, tested with the official app
    
    #plt.tight_layout()
    # Gives more lateral space and makes it easier to scan
        

    for ax, image in zip(axes.flat, images):
    # Scanning each axis after flattenting the subplots + looping images
    
        ax.imshow(image, cmap='gray')
        # Seting grayscale image of each QR code to each axis point
        
    for ax in axes.flat:
    # Scanning each axis after flattenting the subplots
    
        ax.axis('off')
        # Turning off axis seperately to prevent random grids from showing up
        
    plt.show()

########################
def all_data_to_QR(data):
    
    
    #Setting intial values
    tracker = 0
    # This value will determine if 10 codes have been transferred
    
    images = []
    # This is where we store the images until printed
    
    
    print(pyfiglet.figlet_format(data[0]))
    # Printing the title with largness
    
    for item in data[1:]:
    # Looping through each code in 'data'

        
        
        if " " in item:
        # Checking to see if title or expansion name was mentioned

            tracker = 0
            # Setting the tracker back to 0 to restart the chain for the next expansion

            print(' ')
            # Adding space

            print("="*20)
            # Adding seperator from previous QR chunk

            print(' ')
            # Adding space

            plot_multi_QR(images)
            # Running function to print the QR chunk

            images=[]
            # Resetting images for the next QR chunk

            print(' ')
            print('#'*40)
            # Adding seperator

            print(pyfiglet.figlet_format(item))
            # Printing expansion name in large font
        
        
        
        else:
        # If item is not an expansion name
            
            if tracker == 10:
            # Check if the current item is the 10th data chunk
                
                tracker = 0
                # Reset tracker for next data chunk
                
                print(' ')
                print("="*20)
                print(' ')
                
                
                images.append(create_QR(item))
                # Add the current QR code to images
                
                plot_multi_QR(images)
                # Print the QR chunk
                
                images=[]
                # Reset images for the next QR chunk
                
            else:
            # if this is not the 10 QR code
            
                tracker += 1
                # Increase tracker
                
                images.append(create_QR(item))
                # Add current QR code to images

    
    


########################