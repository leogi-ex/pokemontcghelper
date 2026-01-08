
# Importing Libraries

import qrcode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pyfiglet


# Defining functions
## For full breakdown, see: Create QR Codes


##########################
#  def fixing_PTCGL_codes(base_data):
    
#     base_data_list = base_data.split('\n')
#     # Splitting all the gaps between codes
    
#     str_list = list(filter(None, base_data_list))
#     # Removes empty rows if needed 
    
#     str_list = [x.strip(' ') for x in str_list]
#     # Deleting all spaces
    
#     return str_list

########################


def fixing_PTCGL_codes(base_data):
    
    base_data_list = base_data.split('  ')
    # Splitting all the gaps between codes
    
    str_list = list(filter(None, base_data_list))
    # Removes empty rows if needed 
    
    #str_list = [x.strip(' ') for x in str_list]
    # Deleting all spaces
    
    return str_list


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
def plot_multi_QR(ctx, images):
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
        
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    ctx.send(file=discord.File(buffer, 'plot.png'))

########################
def all_data_to_QR(ctx, data):
    
    
    #Setting intial values
    tracker = 0
    # This value will determine if 10 codes have been transferred
    
    images = []
    # This is where we store the images until printed
    
    
    ctx.send(data[0])
    # Printing the title with largness
    
    for item in data[1:]:
    # Looping through each code in 'data'

        
        
        if " " in item:
        # Checking to see if title or expansion name was mentioned

            tracker = 0
            # Setting the tracker back to 0 to restart the chain for the next expansion

            plot_multi_QR(ctx, images)
            # Running function to print the QR chunk

            images=[]
            # Resetting images for the next QR chunk

            ctx.send(pyfiglet.figlet_format(item))
            # Printing expansion name in large font
        
        
        
        else:
        # If item is not an expansion name
            
            if tracker == 10:
            # Check if the current item is the 10th data chunk
                
                tracker = 0
                # Reset tracker for next data chunk
                
                images.append(create_QR(item))
                # Add the current QR code to images
                
                plot_multi_QR(ctx, images)
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