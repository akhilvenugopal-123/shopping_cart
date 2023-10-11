from django.shortcuts import render , get_object_or_404,redirect
from .models import Product, CartItem
from django.http import JsonResponse


# Create your views here.

#  List of products
static_products = [
    {   
        'serial_number': 1,
        'name': 'Table',
        'detail':'This elegant dining table is perfect for hosting family gatherings and dinner parties. With a sturdy wooden construction, it features a beautiful walnut finish that adds warmth and sophistication to your dining space. The table comfortably seats six people, making it ideal for large meals and celebrations. Its sleek and modern design complements a variety of interior styles, from contemporary to traditional. Upgrade your dining area with this stylish table that combines functionality and aesthetics.',
        'amount': 25000,
        
    },
    {   
        'serial_number': 2,
        'name': 'Sofa set',
        'detail': 'Upgrade your living room with this luxurious sofa set that combines comfort and style. This set includes a spacious three-seater sofa, a cozy two-seater loveseat, and a matching single-seater armchair. Crafted with a sturdy wooden frame and upholstered in high-quality, soft velvet fabric, these pieces are designed for ultimate relaxation. The deep cushioning and ergonomic design provide excellent support, making them perfect for long hours of lounging, entertaining, or movie nights. The elegant and timeless design features rolled arms, tufted backrests, and polished wooden legs, adding a touch of sophistication to your home decor.',

        'amount': 23000,
        
    },
    {
        'serial_number' : 3,
        'name' : 'Wooden Chair Set',
        'detail': 'Add a touch of rustic charm to your home with this beautifully crafted wooden chair. Made from solid oak wood, this chair is not only sturdy and durable but also showcases the natural grain and warmth of the wood. Its classic design features a gently curved backrest and a contoured seat for ergonomic comfort. Its compact size makes it easy to fit into any space, while the rich wood finish adds a warm and inviting atmosphere to your home. Elevate your interior decor with this elegant and functional wooden chair. ',

        'amount' : 10500,
        
    },
    {
        'serial_number' : 4,
        'name' : 'Computer Table',
        'detail': 'Enhance your workspace with this modern computer table designed for efficiency and style. Crafted from high-quality engineered wood, this table offers durability and a sleek appearance. Its spacious tabletop provides ample room for your computer, monitor, keyboard, and accessories, ensuring you have a clutter-free and organized workspace. The built-in cable management system keeps your wires and cables neatly tucked away. The table also features a sliding keyboard tray for ergonomic typing and a dedicated shelf for your CPU tower or storage. With its minimalist design and clean lines, this computer table complements any home office or study.',

        'amount' : 14000,
        
    },
    {
        'serial_number' : 5,
        'name' : 'Computer chair',
        'detail': 'Elevate your comfort and productivity with this ergonomic computer chair designed for long hours of work or gaming. Featuring a contoured high-back design, this chair provides excellent lumbar support and promotes proper posture. The adjustable headrest and armrests allow you to customize the chair to your preferred comfort level.Its modern design with sleek lines and a variety of color options adds a stylish touch to your home office or gaming setup. Upgrade your seating experience with this ergonomic computer chair and stay comfortable during extended sessions.',
        'amount' : 5600,
        
    },

    
]


    # For listing products
def product_list(request):
    return render(request, 'product_list.html', {'products': static_products})

    # For detailed view
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_details.html', {'product': product})


   # For cart operations
def view_cart(request):
    cart_items = CartItem.objects.all()  # Fetch all cart items from the database
    total = sum(item.subtotal() for item in cart_items)  # Calculate the total cart value

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Check if the product is already in the cart
    existing_cart_item = CartItem.objects.filter(product=product).first()
    
    if existing_cart_item:
        existing_cart_item.quantity += 1  # Increase the quantity if the product is already in the cart
        existing_cart_item.save()
    else:
        CartItem.objects.create(product=product)  # Create a new cart item if it's not in the cart

    return redirect('product_list')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

def update_cart_quantity(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        new_quantity = int(request.POST.get('new_quantity', 1))  
        cart_item.quantity = new_quantity
        cart_item.save()
        return JsonResponse({'message': 'Cart item quantity updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


 
    # For placing order
def order_confirmation(request):
    # Retrieve the cart items 
    cart_items = CartItem.objects.all()  

    # Calculate the total order amount, considering item quantities
    total_amount = sum(item.product.amount * item.quantity for item in cart_items)

    context = {
        'order_items': cart_items,
        'total_amount': total_amount,
    }

    
    return render(request, 'order_confirmation.html', context)
    

