import React from 'react'
import {
    Flex,
    Text,
    Icon,
    Link,
    Menu,
    MenuButton,
    MenuList
} from '@chakra-ui/react'

const NavItem = ({ icon, title, navSize, handleClick, isModified }) => {
    return (
        <Flex
            align="center"
            mt={1}
            px={3} // Add some horizontal padding
            py={2} // Add some vertical padding
            borderRadius="8px" // Rounded corners
            borderWidth="1px"
            borderColor="#BABABA"
            _hover={isModified ? {} : { bg: '#3B9F8E', cursor: 'pointer' }} // Disable hover effect if modified
            title={title}
            onClick={!isModified ? handleClick : null} // Disable click if isModified is true
            style={{
                opacity: isModified ? 0.5 : 1, // Dim the item if it's disabled
                pointerEvents: isModified ? 'none' : 'auto' // Disable interaction if modified
            }}
        >
            {/* Render the icon */}
            <img
                src={icon}
                boxSize={navSize === "small" ? "1rem" : "1rem"}
                alt={title} // Add alt text for accessibility
                style={{ height: '2rem' }}
            />

            {/* Render the title only if navSize is large */}
            {navSize === "large" && (
                <Text ml={3} fontSize="md" color="white"> {/* Add left margin to separate text from icon */}
                    {title}
                </Text>
            )}
        </Flex>
    );
}

export default NavItem