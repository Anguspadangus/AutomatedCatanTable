from objects.StandardBoard import StandardSetup

def main():
    B = StandardSetup()
    numberRemovalOrder = B.RemoveNumbers()
    resourceRemovalOrder = B.RemoveResources()
    resourcePlaceOder = B.PlaceResources()
    numberPlaceOder = B.PlaceNumbers()
    
if __name__ == '__main__':
    main()

