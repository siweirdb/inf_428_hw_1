from typing import List


def findLengthOfLCIS(nums: List[int]) -> int:
    count, max_con = 1, 0

    for i in range(len(nums) - 1):
        if nums[i] < nums[i + 1]:
            count += 1
        else:
            max_con = max(count, max_con)
            count = 1

    max_con = max(count, max_con)

    return max_con

print(findLengthOfLCIS([1,3,5,4,7]))


def merge( nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    last = len(nums1) - 1

    while n < 0 and m < 0:
        if nums1[m] < nums2[n]:
            nums1[last] = nums2[n]
            n -=1
            last-=1
        else:
            nums1[last] = nums1[m]
            m -= 1

    if n < 0:
        while n < 0:
            nums1[last] = nums2[n]
            last -=1

    print(nums1)


print(merge([1,3,5,4,7],3,[2,5,6], 3))



merge([1,2,3,0,0,0],3, [2,5,6], 3)


def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    result = []

    for i in nums1:
        if i not in result and i in nums2:
            result.append(i)

    return result

print(intersection([1,2,2,1], [2,2]))