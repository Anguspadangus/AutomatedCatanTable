from objects.StandardBoard import StandardSetup

"""
Validating that each of the core functions produce no errors
"""
def main():
    B = StandardSetup()
    numberRemovalOrder = B.RemoveNumbers()
    resourceRemovalOrder = B.RemoveResources()
    resourcePlaceOder = B.PlaceResources()
    numberPlaceOder = B.PlaceNumbers()
    
if __name__ == '__main__':
    main()

